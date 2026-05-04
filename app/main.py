from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.handlers import register_exception_handlers

# Load models so relationships/metadata are registered when using tooling (optional)
from app.db import models as _models  # noqa: F401

app = FastAPI(title="native-ecommerce-be", version="1.0.0")

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["system"])
def read_root():
    return {"message": "Native E‑Commerce API", "docs": "/docs"}
