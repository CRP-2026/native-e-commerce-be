from fastapi import APIRouter

from app.features.auth.router import router as auth_router
from app.features.orders.router import router as orders_router
from app.features.products.router import router as products_router
from app.features.users.router import router as users_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(orders_router, prefix="/orders", tags=["orders"])
