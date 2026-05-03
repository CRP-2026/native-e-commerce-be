from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.database import Base, engine

# Lệnh này sẽ tự động tạo bảng trong DB nếu chưa có 
# (Lưu ý: Đi làm thực tế sẽ dùng Alembic, nhưng giờ test MVP thì cứ dùng cái này cho nhanh)
Base.metadata.create_all(bind=engine)

# Khởi tạo App
app = FastAPI(title="Style UP Store API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn toàn bộ router của dự án vào tiền tố /api/v1
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["System"])
def read_root():
    return {"message": "Success! Chúc mừng dự án Native E-Commerce bắt đầu!"}