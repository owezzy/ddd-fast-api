# PACKAGE: ddd_fast_api

Main application package. Five-layer architecture with strict dependency rules.

## LAYERS

| Layer | Purpose | Can Import |
|-------|---------|------------|
| `entrypoints/` | HTTP, CLI, startup | application, foundation |
| `application/` | Use cases, transactions | domain, foundation |
| `domain/` | Business rules, ports | nothing (pure Python) |
| `infrastructure/` | Persistence, external | domain, foundation |
| `foundation/` | Utilities | nothing (project-independent) |

## COMPOSITION ROOT

`bootstrap.py` is the only file that knows all concrete implementations:
- Creates FastAPI app with lifespan
- Wires settings, logging, exception handlers
- Includes routers
- Manages engine/session lifecycle

## ADDING A NEW DOMAIN

1. Create `domain/<slice>/` with entities, value objects, repository port
2. Create `application/<slice>/` with use cases
3. Create `infrastructure/persistence/repositories/<slice>/` implementing port
4. Add routes in `entrypoints/http/`
5. Wire in `bootstrap.py` or dependency modules
6. Add architecture test coverage in `tests/architecture/`

## MODULE FILES

- `domain/<slice>/__init__.py` — Public API: entities, ports, value objects
- `application/<slice>/__init__.py` — Public API: use case classes
- `infrastructure/persistence/repositories/<slice>/` — Adapter implementations
