# Domain Scaffolding Contract

This project intends to ship a domain-scaffolding workflow during the template
experience phase. The goal is to generate only consistent architectural seams,
never business rules.

## What generation should create

For a new domain slice such as `orders` or `pricing`, the generator should
create:

- domain package and exports;
- application use case package and exports;
- entrypoint dependency and route registration seams;
- transport schemas for HTTP boundaries when requested;
- repository port and persistence adapter seams;
- unit, integration, and architecture test placeholders;
- registration hooks in the composition root or feature wiring layer.

## What generation must not create

- fake business rules;
- unnecessary aggregates or domain events;
- hidden framework abstractions;
- direct infrastructure imports into domain or application code;
- code that fails formatting, typing, or the architecture tests on generation.

## Target generated shape

```text
src/ddd_fast_api/
├── domain/<slice>/
├── application/<slice>/
├── entrypoints/http/
├── infrastructure/persistence/
└── bootstrap.py

tests/
├── unit/
├── integration/
└── architecture/
```

## Success criteria for the future generator

- Generated code is removable without side effects.
- Generated code passes `make format`, `make lint`, `make type-check`, and
  `make test` immediately.
- The output follows the same dependency direction as the catalog reference
  slice.
- The workflow supports structure creation first, with humans filling in domain
  rules afterward.

## Current status

The generator is not implemented yet. This document exists so contributors can
build it against a clear contract rather than inventing one ad hoc.
