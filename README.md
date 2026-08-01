# CALIM Backend

Backend REST API built with

- Flask
- PostgreSQL
- SQLAlchemy
- JWT Authentication

## Installation

```bash
git clone <repo>
```

```bash
cd calim-backend
```

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

## Setup

Create a `.env` file if you need custom values for:

- `DATABASE_URL`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_USE_TLS`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`

If you are using Flask-Migrate with a database, run:

```bash
flask db init
flask db migrate
flask db upgrade
```

If you are using the default SQLite database, the app will create it automatically when started.

## Running locally

Start the app with:

```bash
python app.py
```

Optionally, set a different port:

```bash
PORT=5001 python app.py
```

## Seed data

The app automatically creates initial collections and products if the database is empty.

To reseed users and collections, run:

```bash
python seed.py
```

## API endpoints

- `GET /api/products` — list all products
- `GET /api/products/<id>` — get one product
- `GET /api/collections` — list collections
- `GET /api/collections/<id>` — get one collection
- `POST /api/auth/register` — register a user
- `POST /api/auth/login` — login and receive JWT
- `GET /api/auth/profile` — get current user profile (requires JWT)

## Notes

- The backend exposes CORS for `/api/*`.
- The default database is SQLite at `calim_dev.db` when `DATABASE_URL` is not set.
- Admin and product routes require a valid JWT with `role: admin`.
