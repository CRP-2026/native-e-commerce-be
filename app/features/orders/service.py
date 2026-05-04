from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.db.models import (
    Address,
    Order,
    OrderItem,
    OrderTimeline,
    PaymentMethod,
    Product,
    ProductVariant,
)
from app.features.orders.schemas import OrderCreateIn


def _payment_title(db: Session, store_id: int, code: str) -> str:
    pm = db.execute(
        select(PaymentMethod.title).where(
            PaymentMethod.store_id == store_id,
            PaymentMethod.code == code,
        )
    ).scalar_one_or_none()
    return pm or code


def list_order_summaries(
    db: Session, store_id: int, user_id: str, *, status: str | None
) -> list[dict]:
    q = (
        select(Order)
        .where(Order.store_id == store_id, Order.user_id == user_id)
        .order_by(Order.placed_at.desc())
    )
    if status:
        q = q.where(Order.status == status)  # type: ignore[comparison-overlap]
    orders = db.execute(q).scalars().all()
    ids = [o.id for o in orders]
    if not ids:
        return []
    count_rows = db.execute(
        select(OrderItem.order_id, func.coalesce(func.sum(OrderItem.quantity), 0)).where(
            OrderItem.order_id.in_(ids)
        ).group_by(OrderItem.order_id)
    ).all()
    counts = {oid: int(c) for oid, c in count_rows}
    return [
        {
            "id": o.id,
            "code": o.code,
            "date": o.placed_at.replace(tzinfo=timezone.utc).isoformat(),
            "status": str(o.status),
            "total": float(o.total),
            "itemCount": counts.get(o.id, 0),
        }
        for o in orders
    ]


def get_order_detail(db: Session, store_id: int, user_id: str, order_id: str) -> dict | None:
    o = db.execute(
        select(Order).where(Order.id == order_id, Order.store_id == store_id, Order.user_id == user_id)
    ).scalar_one_or_none()
    if o is None:
        return None

    lines = db.execute(
        select(OrderItem).where(OrderItem.order_id == o.id).order_by(OrderItem.created_at)
    ).scalars().all()
    timelines = db.execute(
        select(OrderTimeline)
        .where(OrderTimeline.order_id == o.id)
        .order_by(OrderTimeline.position, OrderTimeline.happened_at)
    ).scalars().all()

    pm_label = _payment_title(db, store_id, o.payment_method_code)
    estimated = ""
    if o.estimated_delivery_at:
        estimated = o.estimated_delivery_at.replace(tzinfo=timezone.utc).isoformat()

    return {
        "id": o.id,
        "code": o.code,
        "date": o.placed_at.replace(tzinfo=timezone.utc).isoformat(),
        "status": str(o.status),
        "total": float(o.total),
        "items": [
            {
                "id": li.id,
                "name": li.name_snapshot,
                "price": float(li.unit_price),
                "quantity": li.quantity,
                "image": li.image_snapshot,
            }
            for li in lines
        ],
        "shippingAddress": {
            "name": o.ship_name,
            "phone": o.ship_phone,
            "address": o.ship_address,
            "city": o.ship_city,
        },
        "paymentMethod": pm_label,
        "tracking": o.tracking_number or "",
        "estimatedDelivery": estimated,
        "timeline": [
            {
                "status": t.status_label,
                "date": t.happened_at.replace(tzinfo=timezone.utc).isoformat(),
                "completed": t.completed,
            }
            for t in timelines
        ],
    }


def create_order(db: Session, store_id: int, user_id: str, payload: OrderCreateIn) -> dict:
    addr = db.execute(
        select(Address).where(
            Address.id == payload.shipping_address_id,
            Address.store_id == store_id,
            Address.user_id == user_id,
            Address.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if addr is None:
        raise AppError("bad_request", "Invalid shipping address", status_code=400)

    pm = db.execute(
        select(PaymentMethod).where(
            PaymentMethod.store_id == store_id,
            PaymentMethod.code == payload.payment_method_code,
            PaymentMethod.enabled.is_(True),
        )
    ).scalar_one_or_none()
    if pm is None:
        raise AppError("bad_request", "Invalid payment method for this store", status_code=400)

    lines: list[dict] = []
    subtotal = Decimal("0")
    now = datetime.now(timezone.utc)

    for ln in payload.items:
        prod = db.execute(
            select(Product).where(
                Product.store_id == store_id,
                Product.id == ln.product_id,
                Product.deleted_at.is_(None),
                Product.is_active.is_(True),
            )
        ).scalar_one_or_none()
        if prod is None:
            raise AppError("bad_request", f"Unknown product {ln.product_id}", status_code=400)

        variant: ProductVariant | None = None
        if ln.variant_id:
            variant = db.execute(
                select(ProductVariant).where(
                    ProductVariant.store_id == store_id,
                    ProductVariant.product_id == ln.product_id,
                    ProductVariant.id == ln.variant_id,
                    ProductVariant.deleted_at.is_(None),
                )
            ).scalar_one_or_none()
            if variant is None:
                raise AppError(
                    "bad_request",
                    f"Unknown variant {ln.variant_id} for product {ln.product_id}",
                    status_code=400,
                )

        master = prod.sale_price if prod.sale_price is not None else prod.base_price
        master_f = Decimal(str(master))
        if variant is not None:
            unit = Decimal(str(variant.price)) if variant.price is not None else master_f
            sku = variant.sku
            image = variant.image or prod.default_image
            attrs = {"color": variant.color, "size": variant.size}
        else:
            unit = master_f
            sku = prod.id
            image = prod.default_image
            attrs = {}

        if unit <= 0:
            raise AppError("bad_request", "Invalid unit price", status_code=400)

        qty_int = ln.quantity
        qty = Decimal(qty_int)
        line_total = (unit * qty).quantize(Decimal("0.01"))
        subtotal += line_total
        lines.append(
            {
                "product_id": prod.id,
                "variant_id": variant.id if variant else None,
                "name": prod.name,
                "image": image,
                "sku": sku,
                "attrs": attrs or None,
                "unit": unit,
                "qty": qty_int,
                "line_total": line_total,
            }
        )

    ship = payload.shipping_fee
    disc = payload.discount_total
    total = subtotal + ship - disc
    if total < 0:
        raise AppError("bad_request", "Negative order total", status_code=400)

    oid = str(uuid.uuid4())
    code = f"ORD-{now.strftime('%Y%m%d%H%M%S')}-{oid.split('-')[0].upper()}"

    order = Order(
        id=oid,
        store_id=store_id,
        user_id=user_id,
        code=code,
        status="pending",
        placed_at=now,
        subtotal=subtotal,
        shipping_fee=ship,
        discount_total=disc,
        total=total,
        currency="VND",
        payment_method_code=payload.payment_method_code,
        payment_status="unpaid",
        ship_name=addr.name,
        ship_phone=addr.phone,
        ship_address=addr.address,
        ship_city=addr.city,
        ship_address_id=addr.id,
        tracking_number=None,
        estimated_delivery_at=now + timedelta(days=7),
        notes=None,
    )
    db.add(order)
    db.flush()

    for li in lines:
        item = OrderItem(
            id=str(uuid.uuid4()),
            store_id=store_id,
            order_id=oid,
            product_id=li["product_id"],
            variant_id=li["variant_id"],
            name_snapshot=li["name"],
            image_snapshot=li["image"],
            sku_snapshot=li["sku"],
            variant_attrs_snapshot=li["attrs"],
            unit_price=li["unit"],
            quantity=li["qty"],
            line_total=li["line_total"],
        )
        db.add(item)

    t1 = OrderTimeline(
        id=str(uuid.uuid4()),
        store_id=store_id,
        order_id=oid,
        status_label="Order Placed",
        status_code="pending",
        happened_at=now,
        completed=True,
        position=0,
    )
    t2 = OrderTimeline(
        id=str(uuid.uuid4()),
        store_id=store_id,
        order_id=oid,
        status_label="Processing",
        status_code="processing",
        happened_at=now,
        completed=False,
        position=1,
    )
    db.add(t1)
    db.add(t2)
    db.commit()

    detail = get_order_detail(db, store_id, user_id, oid)
    assert detail is not None
    return detail
