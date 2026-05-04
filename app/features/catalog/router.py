from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_store_id
from app.core.exceptions import AppError
from app.features.catalog import service as catalog_svc

router = APIRouter()


@router.get("/categories")
def categories(
    db: Session = Depends(get_db),
    store_id: Annotated[int, Depends(get_store_id)] = 1,
) -> list[dict]:
    return catalog_svc.list_categories(db, store_id)


@router.get("/products")
def products(
    db: Session = Depends(get_db),
    store_id: Annotated[int, Depends(get_store_id)] = 1,
    category_id: str | None = Query(default=None),
    min_price: float | None = Query(default=None),
    max_price: float | None = Query(default=None),
    search: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[dict]:
    return catalog_svc.list_products(
        db,
        store_id,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        search=search,
        limit=limit,
        offset=offset,
    )


@router.get("/products/{product_id}")
def product_detail(
    product_id: str,
    db: Session = Depends(get_db),
    store_id: Annotated[int, Depends(get_store_id)] = 1,
) -> dict:
    row = catalog_svc.get_product(db, store_id, product_id)
    if row is None:
        raise AppError("not_found", "Product not found", status_code=404)
    return row
