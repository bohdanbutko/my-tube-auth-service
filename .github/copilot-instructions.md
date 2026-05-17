## Project Context

- This repo is an authentication microservice for a YouTube-like application called "MyTube".
- Each microservice (auth-service, user-service, video-streaming-service, video-upload-service, web-client) is a separate repository and workspace.
- Architecture: Domain-Driven Design (DDD), Command Query Responsibility Segregation (CQRS), Event Sourcing, Test-Driven Development (TDD), and Event-Driven Development (EDD).
- Kubernetes is used for deployment; Docker is used for containerization.
- Built with Python and FastAPI.

## Structure & Packaging

- Source code is under the `src` directory:
  - `src/domain`: Domain models, entities, value objects, domain services.
  - `src/application`: Application services, commands, queries, handlers.
  - `src/infrastructure`: Database access, external API clients, infrastructure code.
  - `src/api`: API routes, controllers, interface-related code.
- Tests are in the `tests` directory, mirroring the `src` structure.
- `uv` is used for dependency management and locking; `pyproject.toml` and `uv.lock` are the source of truth.
- All package and internal directories should have `__init__.py` files for reliable imports.
- Python version is defined in `pyproject.toml`.
- Dockerfiles and Kubernetes manifests are in the `deploy` directory, organized by environment (e.g., `deploy/dev`, `deploy/prod`).
- CI/CD GitHub Actions are in `.github/workflows`, with separate workflows for testing, building, and deploying.

## Best Practices

- Follow DDD: keep domain logic in `src/domain/`, application logic in `src/application/`, infrastructure code in `src/infrastructure/`.
- Use TDD: write tests in the `tests/` directory before implementing functionality in `src/`.
- Use CQRS: separate commands and queries in `src/application/commands/` and `src/application/queries/`.
- Use EDD: design the system around events, with event handlers in `src/application/event_handlers/`.
- Use FastAPI for the API, with routes in `src/api/`.
- Use event sourcing for persisting state changes, with event store implementations in `src/infrastructure/`.

## Tooling

- `uv` virtual environment is created in-project (`.venv/`).
- Docker and docker-compose are used for local development and testing.
- Each repository is a standalone microservice, with its own CI/CD pipeline and deployment configuration.

## Kubernetes

- Kubernetes manigests can be defined per microservice (in each repo's `deploy/` directory) for a service-specific configuration.
- Start with per-repository configs for simplicity, and consider a centralized configuration if needed as the project grows.

## GitHub

- `.github/` is for GitHub-specific files (workflows, issue templates, instructions).
- `.github/copilot-instructions.md` contains instructions for GitHub Copilot to ensure code generation adheres to the project's architecture and best practices.
