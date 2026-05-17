## Product Context

- This service is part of a YouTube-like platform called MyTube.
- Each microservice lives in its own repository and workspace.
- This repository is the authentication service.

## Architecture Principles

- Follow Domain-Driven Design (DDD).
- Follow CQRS (commands and queries are separate).
- Follow Event-Driven Development (EDD).
- Follow Test-Driven Development (TDD) when adding new behavior.
- Keep business rules in domain/application layers, not in API or infrastructure glue.

## Tech Stack

- Python
- FastAPI
- Docker and docker-compose
- Kubernetes manifests under deploy directories
- uv for dependency management and lockfiles

## Repository Structure

- src/domain: entities, value objects, domain services, exceptions, repositories contracts
- src/application: commands, queries, handlers, application orchestration
- src/infrastructure: concrete repository/service implementations, external integrations
- src/api: FastAPI routes, schemas, server wiring, exception handlers
- tests: mirrors src structure

## Packaging and Imports

- pyproject.toml and uv.lock are source of truth for dependencies.
- Keep **init**.py files in package directories for reliable imports.
- Preserve existing import style and package boundaries.

## Layering Rules

- domain must not depend on api or infrastructure.
- application can depend on domain.
- infrastructure can depend on domain/application abstractions as needed.
- api can depend on application/domain contracts for wiring.

## Coding Rules

- Prefer small, focused changes.
- Keep naming and style consistent with existing codebase.
- Add concise comments only for non-obvious logic.
- Do not introduce broad refactors unless requested.
- Do not break existing public behavior unless explicitly asked.

## Testing Rules

- Add or update tests for behavior changes.
- Keep tests colocated in mirrored test folders.
- Run tests with uv-based workflow.

## Tooling and Commands

- Install/sync dependencies with uv sync.
- Run tests with uv run pytest tests.
- Use lockfile-aware workflow with uv.lock.
- Keep Docker and CI commands aligned with uv usage.

## CI/CD Expectations

- Workflows are under .github/workflows.
- Changes to dependency or runtime flow should keep CI reproducible.
- Prefer deterministic, frozen installs where appropriate.

## Safety and Change Management

- Never revert unrelated user changes.
- If unexpected modifications appear, stop and ask for direction.
- Avoid destructive git commands unless explicitly requested.
- Keep edits minimal and scoped to the request.

## Output Expectations

- Explain what changed and why.
- Call out tradeoffs, risks, and follow-up steps when relevant.
- For reviews, prioritize concrete findings, regressions, and missing tests.
