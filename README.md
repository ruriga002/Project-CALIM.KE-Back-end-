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

Create `.env`

```bash
flask db init
```

```bash
flask db migrate
```

```bash
flask db upgrade
```

```bash
python app.py
```