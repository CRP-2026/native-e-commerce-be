# native-e-commerce-be

Backend FastAPI cho Native E-Commerce, triển khai theo vertical slice và dùng PostgreSQL.

## Current Status

- API base: `/api/v1`
- Health: `GET /api/v1/health`
- Slices đã xong:
  - Catalog: categories + products list/detail/filter
  - Auth + users/me
  - Addresses CRUD
  - Orders + order_items + timeline
- Error format thống nhất:
  - `{ "error": { "code": "...", "message": "...", "details": ... } }`
- Validation:
  - Request validation 422 qua FastAPI/Pydantic
  - JWT lỗi -> 401 chuẩn hóa qua global handler

## Main Endpoints

- `GET /api/v1/categories`
- `GET /api/v1/products?category_id=&min_price=&max_price=&search=&limit=&offset=`
- `GET /api/v1/products/{product_id}`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/users/me` (Bearer token)
- `GET /api/v1/addresses/` (Bearer token)
- `GET /api/v1/addresses/{address_id}` (Bearer token)
- `POST /api/v1/addresses/` (Bearer token)
- `PUT /api/v1/addresses/{address_id}` (Bearer token)
- `DELETE /api/v1/addresses/{address_id}` (Bearer token)
- `GET /api/v1/orders/` (Bearer token)
- `GET /api/v1/orders/{order_id}` (Bearer token)
- `POST /api/v1/orders/` (Bearer token)

## Auth / Multi-store Headers

- `Authorization: Bearer <token>` cho route protected.
- `X-Store-Id`:
  - optional, default `1`
  - token chứa `sid` và sẽ bị reject nếu không khớp `X-Store-Id`.

## Run With Docker (recommended)

```bash
docker compose up -d --build
```

Compose sẽ:
- chạy API tại `http://localhost:8000`
- chạy Postgres tại `localhost:5432`
- init schema + seed khi volume rỗng:
  - `database/init_database.sql`
  - `database/seed_dev.sql`

Nếu cần reset DB init scripts:

```bash
docker compose down -v
docker compose up -d --build
```

## Run Local (venv)

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Environment

`native-e-commerce-be/.env`:

- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM` (default HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`

## Seed Demo Account

Từ `database/seed_dev.sql`:

- email: `demo.jewelry@gmail.com`
- password: `demo123456`
- store: `1`

## SQL Versioning

- Baseline: `database/migrations/0001_baseline.sql`
- Init hiện hành: `database/init_database.sql`
- Dev seed: `database/seed_dev.sql`

Hiện đang theo hướng migration SQL thủ công; có thể chuyển Alembic full trong bước tiếp theo.

## Notes

- Hash password đang dùng `bcrypt` trong code.
- CORS đang mở `*` cho dev.
- `requirements.txt` hiện còn `passlib[bcrypt]` để tương thích cũ; flow hiện tại dùng `bcrypt` trực tiếp.
# native-e-commerce-be

Backend FastAPI cho Native E-Commerce, đã triển khai theo vertical slice và dùng PostgreSQL.

## Current Status

- API base: `/api/v1`
- Health: `GET /api/v1/health`
- Slices đã xong:
  - Catalog: categories + products list/detail/filter
  - Auth + users/me
  - Addresses CRUD
  - Orders + order_items + timeline
- Error format thống nhất:
  - `{ "error": { "code": "...", "message": "...", "details": ... } }`
- Validation:
  - Request validation 422 qua FastAPI/Pydantic
  - JWT lỗi -> 401 chuẩn hóa qua global handler

## Main Endpoints

- `GET /api/v1/categories`
- `GET /api/v1/products?category_id=&min_price=&max_price=&search=&limit=&offset=`
- `GET /api/v1/products/{product_id}`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/users/me` (Bearer token)
- `GET /api/v1/addresses/` (Bearer token)
- `GET /api/v1/addresses/{address_id}` (Bearer token)
- `POST /api/v1/addresses/` (Bearer token)
- `PUT /api/v1/addresses/{address_id}` (Bearer token)
- `DELETE /api/v1/addresses/{address_id}` (Bearer token)
- `GET /api/v1/orders/` (Bearer token)
- `GET /api/v1/orders/{order_id}` (Bearer token)
- `POST /api/v1/orders/` (Bearer token)

## Auth / Multi-store Headers

- `Authorization: Bearer <token>` cho route protected.
- `X-Store-Id`:
  - optional, default `1`
  - token chứa `sid` và sẽ bị reject nếu không khớp `X-Store-Id`.

## Run With Docker (recommended)

```bash
docker compose up -d --build
```

Compose sẽ:
- chạy API tại `http://localhost:8000`
- chạy Postgres tại `localhost:5432`
- init schema + seed khi volume rỗng:
  - `database/init_database.sql`
  - `database/seed_dev.sql`

Nếu cần reset DB init scripts:

```bash
docker compose down -v
docker compose up -d --build
```

## Run Local (venv)

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Environment

`native-e-commerce-be/.env`:

- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM` (default HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`

## Seed Demo Account

Từ `database/seed_dev.sql`:

- email: `demo@jewelry.local`
- password: `demo123456`
- store: `1`

## SQL Versioning

- Baseline: `database/migrations/0001_baseline.sql`
- Init hiện hành: `database/init_database.sql`
- Dev seed: `database/seed_dev.sql`

Hiện đang theo hướng migration SQL thủ công; có thể chuyển Alembic full trong bước tiếp theo.

## Notes

- Hash password đang dùng `bcrypt` trong code.
- CORS đang mở `*` cho dev.
- `requirements.txt` hiện còn `passlib[bcrypt]` để tương thích cũ; flow hiện tại dùng `bcrypt` trực tiếp.

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

1. Tạo `.env` từ mẫu (nếu chưa có): `cp .env.example .env` và điền `SECRET_KEY` cố định cho dev.

2. Chạy API + PostgreSQL (schema được tạo tự động lần đầu nhờ mount `../database/init_database.sql` vào `docker-entrypoint-initdb.d`):

```bash
docker compose up -d --build
```

Chỉ DB (ví dụ bạn chạy FastAPI local): `docker compose up -d db`. Lần đầu volume `postgres_data` rỗng, container sẽ chạy script init; nếu đổi `init_database.sql` sau khi DB đã có dữ liệu, cần `docker compose down -v` (xóa volume) rồi `up` lại.

Trong Compose, service `api` ghi đè `DATABASE_URL` trỏ tới host `db`; khi chạy `uvicorn` trên máy, dùng `DATABASE_URL=...@localhost:5432/...` trong `.env`.

3. Cài dependencies (nếu chạy local):

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux / macOS
# source .venv/bin/activate
pip install -r requirements.txt
```

4. Chạy ứng dụng (hot-reload):

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Environment**

File `.env.example` là mẫu; copy thành `.env`:

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` — dùng cho service `db` trong Compose (có giá trị mặc định trong `docker-compose.yml` nếu thiếu).
- `DATABASE_URL` — khi chạy API **local**: `postgresql://...@localhost:5432/...`
- `SECRET_KEY` — JWT
- `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` — JWT (khớp `app/core/config.py`)

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