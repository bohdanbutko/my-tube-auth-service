## Project Context

- This repo is the authentication microservice for a YouTube-like application called "MyTube".
- Each microservice is a separate repository and workspace:
  - auth-service
  - user-service
  - video-streaming-service
  - video-upload-service
  - web-client
- Built with Python and FastAPI.
- Architecture uses Domain-Driven Design (DDD), CQRS, Event Sourcing, TDD, and Event-Driven Development.
- Docker is used for containerization.
- Kubernetes is used for deployment.

## Structure & Packaging

- Source code is under `src/`:
  - `src/domain/`: domain models, entities, value objects, domain services, domain events.
  - `src/application/`: application services, commands, queries, handlers, event handlers.
  - `src/infrastructure/`: database access, event stores, external clients, framework integrations.
  - `src/api/`: FastAPI routes, controllers, request/response schemas.
- Tests are under `tests/`, mirroring the `src/` structure.
- `uv` is used for dependency management and locking.
- `pyproject.toml` and `uv.lock` are the source of truth.
- All package and internal directories should have `__init__.py` files.
- Python version is defined in `pyproject.toml`.
- Dockerfiles and Kubernetes manifests are under `deploy/`, organized by environment, such as `deploy/dev/` and `deploy/prod/`.
- GitHub Actions workflows are under `.github/workflows/`.

## Architecture Rules

- Keep domain logic in `src/domain/`.
- Keep application orchestration in `src/application/`.
- Keep infrastructure integrations in `src/infrastructure/`.
- Keep HTTP/API concerns in `src/api/`.
- Do not put FastAPI, database, Kubernetes, Docker, or external service concerns in the domain layer.
- Use CQRS:
  - commands go under `src/application/commands/`
  - queries go under `src/application/queries/`
  - handlers should stay close to their command/query definitions
- Use event-driven design:
  - domain events should describe meaningful business facts
  - event handlers go under `src/application/event_handlers/`
- Use event sourcing for persisted aggregate state changes when implementing lifecycle behavior.
- Preserve existing public APIs unless explicitly asked to change them.

## Testing Rules

- Add or update tests when changing behavior.
- Prefer writing or updating tests before implementation.
- Keep tests focused and close to the corresponding source structure.
- Prefer unit tests for domain and application logic.
- Use integration tests for API, database, event store, and infrastructure behavior.

## Tooling

- Use `uv` for dependency management.
- Do not manually edit dependency versions unless necessary.
- Do not introduce new dependencies without explicit approval.
- The virtual environment is created in-project at `.venv/`.
- Use Docker and docker-compose for local development and testing where applicable.
- Use Ruff for linting and formatting.
- Use `ty` for static type checking.
- Run Ruff checks with `uv run ruff check .`.
- Run Ruff formatting with `uv run ruff format .`.
- Run type checks with `uv run ty check`.

## Kubernetes

- Kubernetes manifests are defined per microservice under `deploy/`.
- Start with per-repository Kubernetes config.
- Do not centralize deployment configuration unless explicitly requested.

## Agent Behavior

- Make minimal, focused changes.
- Preserve DDD, CQRS, and event-sourcing boundaries.
- Prefer explicit, typed Python code.
- Avoid broad rewrites unless explicitly requested.
- Do not add abstractions unless they remove real duplication or protect a clear boundary.
- Run relevant tests after changes when possible.
- Run `uv run ruff check .` after Python changes when possible.
- Run `uv run ty check` after typed Python changes when possible.
- If tests or checks are not run, state why.
- Before finishing, summarize:
  - changed files
  - tests run
  - Ruff results
  - ty results
  - risks or follow-up work

## Commit Messages

- Use Conventional Commits.
- Format commit messages as `<type>(<scope>): <summary>`.
- Use lowercase commit types.
- Use an optional scope when it adds useful context.
- Write the summary in imperative mood.
- Do not end the summary with a period.
- Keep the first line concise, preferably under 72 characters.
- Use the body only when the change needs explanation beyond the summary.

Allowed types:

- `feat`: new user-facing or domain behavior
- `fix`: bug fix
- `refactor`: code restructuring without behavior change
- `test`: adding or updating tests
- `docs`: documentation-only changes
- `style`: formatting-only changes
- `chore`: maintenance, tooling, dependency, or config changes
- `ci`: CI/CD workflow changes
- `build`: build system, Docker, packaging, or dependency-lock changes
- `perf`: performance improvement
