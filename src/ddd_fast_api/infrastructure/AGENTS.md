# INFRASTRUCTURE LAYER

Implements domain ports with concrete adapters.

## RULES

- Implements interfaces defined in `domain/<slice>/repositories.py`
- SQLAlchemy models live here, NOT in domain
- Repositories never call commit — use cases own transactions
- Mapper functions convert between domain entities and ORM models

## STRUCTURE

```
infrastructure/
└── persistence/
    ├── base.py              # SQLAlchemy declarative base
    ├── database.py          # Engine, session factory creation
    ├── models/              # SQLAlchemy ORM models
    │   ├── catalog.py
    │   └── identity.py
    ├── mappers/             # Domain ↔ ORM conversion
    │   ├── catalog.py
    │   └── identity.py
    ├── repositories/        # Repository adapter implementations
    │   ├── catalog.py
    │   └── identity.py
    └── unit_of_work.py      # SQLAlchemy UnitOfWork implementation
```

## ADAPTER SELECTION

Settings-driven seam in `foundation/settings.py`:
- `catalog_repository_backend`: `"memory"` | `"sqlalchemy"`
- `identity_repository_backend`: `"memory"` | `"sqlalchemy"`

Memory adapters for tests/fast startup; SQLAlchemy for PostgreSQL persistence.

## ADDING A NEW ADAPTER

1. Create `infrastructure/persistence/models/<slice>.py` (ORM model)
2. Create `infrastructure/persistence/mappers/<slice>.py` (domain ↔ ORM)
3. Create `infrastructure/persistence/repositories/<slice>.py` (implement port)
4. Add to `unit_of_work.py` if transaction scope needed
5. Wire adapter selection in `bootstrap.py` or dependency module
