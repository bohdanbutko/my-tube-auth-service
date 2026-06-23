# MyTube Auth Service

Authentication and authorization microservice for MyTube, built with FastAPI.

This service provisions auth identities, authenticates credentials, issues JWT
access tokens, and verifies access tokens for other MyTube services.

## Requirements

- Python 3.14 (or another version compatible with `>=3.14,<3.15`)
- `uv` installed: https://docs.astral.sh/uv/
- Docker and Docker Compose, if running the service in a container

## Environment

Use a separate environment file for each runtime:

```bash
cp .env.local.example .env.local
cp .env.docker.example .env.docker
```

Environment variables:

- `JWT_SECRET_KEY`: private server-side secret used to sign and verify JWTs.
- `JWT_ALGORITHM`: JWT signing algorithm. Local default is `HS256`.
- `DATABASE_URL`: optional PostgreSQL connection URL. If it is not set, the
  service uses the in-memory repository.

`.env.local` is used when running the service directly on the host:

```env
DATABASE_URL=postgresql+psycopg://<username>:<password>@localhost:5432/<database_name>
```

`.env.docker` is used by Docker Compose. Because PostgreSQL runs in a separate
container exposed through the host, it uses `host.docker.internal`:

```env
DATABASE_URL=postgresql+psycopg://<username>:<password>@host.docker.internal:5432/<databasename>
```

## Run Locally With uv

Install dependencies:

```bash
uv sync --dev
```

Start the API:

```bash
uv run uvicorn src.api.server:app --host 0.0.0.0 --port 8000 --reload --env-file .env.local
```

## Run With Docker

Build and start the service:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Stop the service:

```bash
docker compose down
```

## API Surface

- `POST /api/v1/identities` provisions an auth identity and stores hashed credentials.
- `POST /api/v1/login` authenticates credentials and returns a JWT access token.
- `GET /api/v1/verify-token` validates an access token and returns its claims.
- `GET /api/v1/health` returns a simple local/internal health check.

### Provision Identity

```http
POST /api/v1/identities
Content-Type: application/json
```

```json
{
  "subject_id": "11111111-1111-4111-8111-111111111111",
  "email": "user@example.com",
  "password": "Password123!",
  "channel_accesses": [
    {
      "channel_id": "22222222-2222-4222-8222-222222222222",
      "role": "owner"
    }
  ]
}
```

### Login

```http
POST /api/v1/login
Content-Type: application/x-www-form-urlencoded
```

```text
username=user@example.com
password=Password123!
```

Successful response:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### Verify Token

```http
GET /api/v1/verify-token
Authorization: Bearer <jwt>
```

### Health

```http
GET /api/v1/health
```

## Run Tests

```bash
uv run pytest tests
```

## Database Migrations

This service uses Alembic for database migrations. `DATABASE_URL` must point to
the auth-service database before running migration commands.

Apply all migrations:

```bash
uv run --env-file .env.local alembic upgrade head
```

Rollback the latest migration:

```bash
uv run --env-file .env.local alembic downgrade -1
```

Show the current migration version:

```bash
uv run --env-file .env.local alembic current
```

## Quality Checks

```bash
uv run ruff check .
uv run ruff format .
uv run ty check
```

## Docker And Kubernetes

The `Dockerfile` defines how to build the service image. Docker Compose is used
for local development only. Kubernetes deployments should use an image built
from this Dockerfile and pushed to a container registry.

## Lockfile

This project uses `uv.lock` as the lockfile.
