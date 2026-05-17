# MyTube Auth Service

Authentication microservice for MyTube, built with FastAPI.

## Requirements

- Python 3.14 (or another version compatible with `>=3.9,<4.0`)
- `uv` installed: https://docs.astral.sh/uv/

## Install Dependencies

```bash
uv sync --dev
```

## Run The API

```bash
uv run uvicorn src.api.server:app --host 0.0.0.0 --port 8000 --reload
```

## Run Tests

```bash
uv run pytest tests
```

## Lockfile

This project uses `uv.lock` as the lockfile and does not use Poetry.
