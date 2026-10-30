# Price Tracker

A backend service that lets users track product prices and get notified when a price drops below their target.

> **Status:** Work in progress. Managing tracked products (CRUD API with validation) is done. Price scraping, scheduled checks, price history and email notifications are planned.

## Tech stack

- **Language & framework:** Python, FastAPI
- **Database:** SQLAlchemy 2.0 with SQLite (PostgreSQL + Alembic planned)
- **Validation:** Pydantic
- **Dev tooling:** ruff (formatting), pytest (testing)

## Running locally

```bash
git clone https://github.com/wei242524/price-tracker.git
cd price-tracker
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/docs to try the API in the browser.

## API

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/products` | Add a product to track (returns 409 if the URL already exists) |
| GET | `/products` | List all tracked products |
| GET | `/products/{id}` | Get one product |
| PATCH | `/products/{id}` | Update a product's URL or target price |
| DELETE | `/products/{id}` | Stop tracking a product |

Target prices must be positive with at most 2 decimal places.