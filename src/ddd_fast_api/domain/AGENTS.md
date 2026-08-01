# DOMAIN LAYER

Core business rules. Zero framework dependencies.

## RULES

- **NO imports** from fastapi, pydantic, sqlalchemy, infrastructure, or entrypoints.
- Use `dataclasses` for entities (not Pydantic BaseModel).
- Value objects are immutable, validated at construction.
- Repository ports are abstract (Protocol or ABC).

## STRUCTURE

```
domain/
├── catalog/
│   ├── entities.py      # CatalogItem entity
│   ├── value_objects.py # SKU, CatalogItemStatus
│   └── repositories.py  # CatalogRepository port, CatalogUnitOfWork port
└── identity/
    ├── entities.py      # UserAccount entity
    ├── value_objects.py # EmailAddress
    └── repositories.py  # IdentityRepository port
```

## PATTERNS

- **Entities:** `@dataclass(slots=True)` with `__post_init__` validation
- **Value objects:** Immutable, validated, meaningful `__eq__` and `__hash__`
- **Repository ports:** `Protocol` classes defining required methods
- **UnitOfWork port:** `__aenter__`/`__aexit__`, `commit()`, `rollback()`
- **Domain errors:** Raise `ValueError` or domain-specific exceptions (not ProjectError)

## ADDING A NEW DOMAIN

1. Create directory `domain/<slice>/`
2. Add `entities.py` with dataclass entities
3. Add `value_objects.py` with validated immutable types
4. Add `repositories.py` with Protocol port definitions
5. Export public API in `__init__.py`
