# PROJECT KNOWLEDGE BASE

**Generated:** 2026-07-20
**Repository:** ddd-fast-api
**Status:** Early scaffold — architecture defined, implementation in progress

## OVERVIEW

Production-oriented FastAPI service template inspired by Ardan Labs Service. Pragmatic DDD with five-layer architecture: Entrypoints → Application → Domain → Infrastructure → Foundation.

## STRUCTURE

```
ddd-fast-api/
├── src/ddd_fast_api/
│   ├── entrypoints/    # FastAPI routes, schemas, HTTP adapters
│   ├── application/    # Use cases, orchestration, transaction boundaries
│   ├── domain/         # Entities, value objects, rules, ports (NO framework imports)
│   ├── infrastructure/ # PostgreSQL repos, auth adapters, external clients
│   ├── foundation/     # Logging, errors, settings (domain-independent)
│   └── bootstrap.py    # Composition root, lifespan, app factory
├── tests/
│   ├── unit/           # Domain + application tests (no DB/HTTP)
│   ├── integration/    # SQLAlchemy/PostgreSQL path tests
│   └── architecture/   # Import boundary enforcement
├── alembic/            # Database migrations
├── docs/               # Architecture plan, ADRs, scaffolding contract
└── Makefile            # Dev commands (sync, run, test, lint, format, type-check)
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add new domain | `domain/<slice>/`, `application/<slice>/` | Mirror across layers |
| Add HTTP endpoint | `entrypoints/http/routes.py` | Use Depends for use cases |
| Add persistence adapter | `infrastructure/persistence/repositories/` | Implement domain port |
| Change settings | `foundation/settings.py` | Pydantic-settings, `DDD_FAST_API_` prefix |
| Modify error handling | `foundation/errors.py` | ProjectError → HTTP 4xx/5xx |
| Add migration | `alembic/versions/` | Use `alembic revision --autogenerate` |
| Architecture tests | `tests/architecture/` | Enforce import boundaries |

## CONVENTIONS

- **Dependency direction:** Domain imports nothing; Application imports Domain; Infrastructure implements Domain ports; Entrypoints depend on Application.
- **Pydantic at boundaries only:** Domain entities are plain dataclasses, not Pydantic models.
- **Repository pattern:** Repositories never commit; use cases own transaction boundaries via UnitOfWork.
- **Async everywhere:** SQLAlchemy async, asyncpg, async use cases.
- **Settings prefix:** All env vars prefixed with `DDD_FAST_API_`.
- **Adapter seam:** `catalog_repository_backend` and `identity_repository_backend` settings switch between `memory` and `sqlalchemy`.

## ANTI-PATTERNS (THIS PROJECT)

- Domain layer MUST NOT import FastAPI, Pydantic, SQLAlchemy, or infrastructure.
- Application layer MUST NOT import FastAPI, SQLAlchemy, or infrastructure.
- Foundation layer MUST NOT import any project business layer.
- Repositories MUST NOT call commit/rollback directly.
- Use Pydantic for API schemas, NOT for domain entities.

## COMMANDS

```bash
make sync           # Install dependencies
make run            # Start dev server (uvicorn)
make test           # Run pytest
make lint           # Ruff check
make format         # Ruff fix + format
make type-check     # mypy src
make hooks          # Install Husky git hooks
make commit         # Commitizen conventional commit
```

## NOTES

- `main.py` at root is compatibility bootstrap for `uv run python main.py`.
- In-memory adapters are default; set `DDD_FAST_API_CATALOG_REPOSITORY_BACKEND=sqlalchemy` for PostgreSQL.
- Architecture tests enforce layer boundaries via AST analysis of imports.
- Beads (bd) is used for issue tracking: `bd ready`, `bd show <id>`, `bd close <id>`.
