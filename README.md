# Price Tracker

A backend service that lets users track product prices and get notified when a price drops below their target.

> **Status:** Work in progress. Managing tracked products (CRUD API with validation) is done. Price scraping, scheduled checks, price history and email notifications are planned.

**Live demo:** https://price-tracker-0ui1.onrender.com/docs

> Hosted on Render's free tier, so the first request after 15 minutes of inactivity can take about a minute while the service wakes up.

## Tech stack

- **Language & framework:** Python, FastAPI
- **Database:** SQLAlchemy 2.0 with SQLite or PostgreSQL, Alembic migrations
- **Infrastructure:** Docker, Docker Compose, Render (hosting), Neon (managed PostgreSQL)
- **Validation:** Pydantic
- **Dev tooling:** ruff (formatting), pytest (testing)

## Running locally

```bash
git clone https://github.com/wei242524/price-tracker.git
cd price-tracker
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
python -m alembic upgrade head
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs to try the API in the browser.

### Using Docker

To run the app and PostgreSQL together without installing Python, use Docker Compose:

```bash
docker compose up --build
```

Then open http://localhost:8000/docs. Migrations run automatically when the app starts.

### Using PostgreSQL

To develop with `--reload` against PostgreSQL, start only the database with Docker Compose and point `DATABASE_URL` at it:

```bash
docker compose up -d db
$env:DATABASE_URL = "postgresql+psycopg://price_tracker:price_tracker@localhost:5432/price_tracker"   # macOS/Linux: export DATABASE_URL=...
python -m alembic upgrade head
uvicorn app.main:app --reload
```

Data is stored in a Docker volume, so it survives `docker compose down`. Use `docker compose down -v` to delete it.

Tests always use an in-memory SQLite database, so they don't need Docker.

### Database migrations

The database schema is managed with Alembic. After changing a model in `app/models.py`, generate a migration and review it before applying:

```bash
python -m alembic revision --autogenerate -m "Describe the change"
python -m alembic upgrade head
```

## Deployment

The app is deployed on [Render](https://render.com) from the `Dockerfile`, and every merge to `main` deploys automatically. The database is a [Neon](https://neon.com) PostgreSQL instance in the same region (Frankfurt), so the app and database stay close to each other.

Render's free PostgreSQL databases are deleted after 30 days, so the database is hosted on Neon instead, keeping the data separate from the app host.

Migrations run on every start (`alembic upgrade head`). This is safe because the command is idempotent: if the database is already at the latest version, it does nothing.

## Configuration

Settings are read from environment variables. See `.env.example` for the full list.

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./price_tracker.db` | Database connection string |
| `PORT` | `8000` | Port the server listens on inside the Docker container (set automatically by Render) |

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
