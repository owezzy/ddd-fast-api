# TESTS

Three test categories with strict separation.

## STRUCTURE

```
tests/
├── unit/                  # Fast, no DB/HTTP
│   ├── test_*_domain.py   # Entity/value object behavior
│   ├── test_*_use_cases.py # Application logic
│   └── test_*_http.py     # Schema validation, response shaping
├── integration/           # Real persistence
│   └── test_*_sqlalchemy_path.py # SQLAlchemy adapter tests
└── architecture/          # Import boundary enforcement
    └── test_domain_import_rules.py
```

## CONVENTIONS

- **Unit tests:** No FastAPI, no database, no network. Pure business logic.
- **Integration tests:** Use SQLAlchemy async with test database.
- **Architecture tests:** AST-based import analysis enforcing layer boundaries.
- **Test files:** Named `test_<module>.py` mirroring source structure.
- **Fixtures:** Defined in `conftest.py` at test root.

## RUNNING

```bash
make test           # All tests
uv run pytest tests/unit/           # Unit only
uv run pytest tests/integration/    # Integration only
uv run pytest tests/architecture/   # Architecture only
```

## WRITING NEW TESTS

- Domain tests: test invariants, validation, business rules
- Use case tests: test orchestration, transaction boundaries
- HTTP tests: test schema validation, error mapping, response shape
- Integration tests: test repository against real PostgreSQL
- Architecture tests: add forbidden import prefixes to `test_domain_import_rules.py`
