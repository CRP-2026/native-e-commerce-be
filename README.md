# native-e-commerce-be

API backend mẫu cho ứng dụng e-commerce (FastAPI).

**Mục tiêu:** cung cấp bộ khung backend nhanh để phát triển tính năng `auth`, `users`, `products`, `orders` và dễ dàng chạy bằng Docker hoặc môi trường ảo Python.

**Cấu trúc chính**

```
native-e-commerce-be/
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── app/
    ├── main.py
    ├── api/router.py
    ├── core/
    │   ├── config.py
    │   ├── database.py
    │   └── security.py
    └── features/
        ├── auth/
        ├── users/
        ├── products/
        └── orders/
```

**Tệp quan trọng**
- `app/main.py`: entrypoint ứng dụng.
- `app/api/router.py`: đăng ký các router với tiền tố `/api/v1`.
- `app/core/config.py`: loader `.env` và cấu hình chung.
- `app/core/database.py`: kết nối SQLAlchemy.

**Yêu cầu**
- Python 3.11+
- PostgreSQL (local hoặc container)
- Thư viện trong `requirements.txt`

**Cách chạy (Docker, khuyến nghị)**

1. Khởi động database bằng Docker Compose:

```bash
docker-compose up -d db
```

2. Cài dependencies (nếu chạy local):

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux / macOS
# source .venv/bin/activate
pip install -r requirements.txt
```

3. Chạy ứng dụng (hot-reload):

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Environment**

Dự án sử dụng file `.env` nằm ở gốc repo. Một mẫu đã có sẵn `.env` với các biến:

- `DATABASE_URL` — chuỗi kết nối PostgreSQL
- `SECRET_KEY` — khóa bí mật JWT
- `JWT_ALGORITHM` — thuật toán JWT (mặc định HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` — thời gian hết hạn token (phút)

**Kiểm tra nhanh API**

Sau khi chạy app, kiểm tra các endpoint:

- Health: `GET /health`
- Auth ping: `GET /api/v1/auth/ping`
- Users ping: `GET /api/v1/users/ping`
- Products ping: `GET /api/v1/products/ping`
- Orders ping: `GET /api/v1/orders/ping`

(Các endpoint ping trả về trạng thái sẵn sàng của module.)

**Migrations**

Alembic đã được thêm vào `requirements.txt`. Để thiết lập migration bạn cần:

```bash
alembic init alembic
# Chỉnh sửa alembic/env.py để import Base từ app.core.database
# Tạo migration: alembic revision --autogenerate -m "create tables"
# Áp dụng migration: alembic upgrade head
```

**Ghi chú phát triển**

- Toàn bộ imports trong `app/` dùng dạng tuyệt đối từ gốc package `app` (ví dụ `from app.core import config`).
- `app/core/config.py` nạp `.env` bằng đường dẫn tuyệt đối tới thư mục gốc repo, giúp clone ở máy khác chạy ổn định.

**Tiếp theo (gợi ý công việc)**
- Hoàn thiện CRUD cho `users`, `products`, `orders` với SQLAlchemy và dependency injection.
- Thêm unit tests và CI.
- Thiết lập Alembic migrations và seed data cho dev.

---

Nếu bạn muốn mình mở rộng `README.md` với phần API spec (OpenAPI / examples) hoặc thêm hướng dẫn migration chi tiết, mình làm tiếp được ngay.