# MyTube Auth Service

Authentication and authorization microservice for MyTube, built with FastAPI.

## Requirements

- Python 3.14 (or another version compatible with `>=3.14,<3.15`)
- `uv` installed: https://docs.astral.sh/uv/

## Install Dependencies

```bash
uv sync --dev
```

## Run The API

```bash
uv run uvicorn src.api.server:app --host 0.0.0.0 --port 8000 --reload
```

## API Surface

- `POST /api/v1/identities` provisions an auth identity and stores hashed credentials.
- `POST /api/v1/login` authenticates credentials and returns a JWT access token.
- `GET /api/v1/verify-token` validates an access token and returns its claims.

## Run Tests

```bash
uv run pytest tests
```

## Lockfile

This project uses `uv.lock` as the lockfile and does not use Poetry.
