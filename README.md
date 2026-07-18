# ddd-fast-api

<p align="center">
  <a href="#repository-status"><img alt="Project status: planning" src="https://img.shields.io/badge/status-planning-blue"></a>&nbsp;
  <a href="https://www.python.org/"><img alt="Python 3.12+" src="https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&amp;logoColor=white"></a>&nbsp;
  <a href="https://github.com/owezzy/ddd-fast-api/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/owezzy/ddd-fast-api"></a>&nbsp;
  <a href="https://github.com/owezzy/ddd-fast-api/forks"><img alt="GitHub forks" src="https://img.shields.io/github/forks/owezzy/ddd-fast-api"></a>&nbsp;
  <a href="https://github.com/owezzy/ddd-fast-api/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/owezzy/ddd-fast-api"></a>&nbsp;
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-yellow.svg"></a>
</p>

An open-source, production-oriented FastAPI service template inspired by
[Ardan Labs Service](https://github.com/ardanlabs/service).

The project translates Ardan's emphasis on explicit boundaries, small mental
models, operational completeness, and domain-oriented design into idiomatic
Python. It is intended to be a starting point, not another framework layered on
top of FastAPI.

> **Project status:** early scaffold. The architecture and delivery roadmap are
> defined, but the FastAPI service and production capabilities are not yet
> implemented. Roadmap items below are deliberately unchecked unless they exist
> in the repository.

## Contents

- [Why this project exists](#why-this-project-exists)
- [Design principles](#design-principles)
- [Target architecture](#target-architecture)
- [Pydantic's role](#pydantics-role)
- [Planned capabilities](#planned-capabilities)
- [Repository status](#repository-status)
- [Getting started](#getting-started)
- [Delivery roadmap](#delivery-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Why this project exists

Many FastAPI examples demonstrate routing and database access but stop before
the concerns that make a service maintainable in production. This template aims
to provide a coherent reference for:

- keeping business rules independent of FastAPI and persistence;
- organizing a modular service around domain language;
- defining explicit transaction and dependency boundaries;
- testing domain behavior without HTTP, PostgreSQL, or network access;
- shipping local and Kubernetes workflows from the same repository;
- providing logs, metrics, traces, health signals, security, and CI by default;
- generating new domain seams without generating business rules.

The initial reference domain will model inventory and catalog management. A
separate identity capability will demonstrate local account signup, user
management, RBAC, and a replaceable external OIDC adapter.

## Design principles

1. **Pragmatic DDD** — use entities, value objects, aggregates, and domain events
   only when they clarify real business rules.
2. **Dependencies point inward** — domain code has no FastAPI, Pydantic,
   SQLAlchemy, or infrastructure imports.
3. **Frameworks stay at the edges** — FastAPI is the HTTP adapter, not the
   application architecture.
4. **Explicit mapping** — transport schemas, domain models, and persistence
   models evolve independently.
5. **Use-case transactions** — the application layer owns commit and rollback;
   repositories never commit independently.
6. **Operations are architecture** — containers, Kubernetes, migrations,
   telemetry, and CI are maintained alongside the service.
7. **Minimal dependencies** — add libraries for demonstrated needs, not for
   hypothetical flexibility.

## Target architecture

The project uses five memorable code layers:

```text
Entrypoints       FastAPI routes, schemas, CLI, startup and shutdown
      │
Application       Use cases, orchestration, authorization, transactions
      │
Domain            Entities, value objects, rules, errors, events and ports
      ▲
Infrastructure    PostgreSQL, authentication and external-service adapters

Foundation        Small domain-independent logging, telemetry and utility code
```

The composition root is the only place that knows every concrete adapter.
Domain modules are mirrored across layers so a feature remains traceable from
HTTP input to business behavior and storage.

The planned repository shape is:

```text
ddd-fast-api/
├── src/ddd_fast_api/
│   ├── entrypoints/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   ├── foundation/
│   └── bootstrap.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   └── architecture/
├── migrations/
├── deploy/
│   ├── compose/
│   └── kubernetes/
├── docs/
├── pyproject.toml
└── Makefile
```

This tree describes the target, not the repository's current contents.

## Pydantic's role

Pydantic will validate and serialize data at system boundaries:

- API request and response schemas;
- OpenAPI generation;
- application configuration through `pydantic-settings`;
- messages exchanged with external systems.

Core domain entities and value objects remain plain Python types or dataclasses.
Explicit mappers translate between Pydantic schemas, domain models, and
SQLAlchemy models. This separation keeps business behavior testable and allows
the HTTP, domain, and persistence representations to evolve independently.

## Planned capabilities

The template targets Python equivalents for the production capabilities shown
by Ardan Labs Service:

- FastAPI and Starlette routing, lifespan, dependencies, and middleware;
- PostgreSQL with SQLAlchemy 2 async, asyncpg, and Alembic;
- CRUD use cases, filtering, ordering, pagination, and stable errors;
- local accounts, JWT/OIDC authentication, RBAC, and object-level policies;
- structured logging, OpenTelemetry, Prometheus-compatible metrics, Tempo, and
  Grafana;
- pytest-based unit, integration, contract, property, architecture, and smoke
  tests;
- locked dependencies with an optional wheelhouse for offline builds;
- multi-stage Docker images and Docker Compose for local development;
- Kustomize-based Kubernetes environments and a separate migration Job;
- GitHub Actions as the default CI/CD implementation, with CircleCI documented
  as an alternative;
- OpenAPI, MkDocs, and source-reference documentation;
- a project template and domain-scaffolding command.

A capability counts as implemented only when code or configuration, automated
tests, user documentation, and a passing CI check all exist.

## Repository status

Currently present:

- Git repository and `main` branch;
- Python project metadata, runtime dependencies, and development tooling
  baseline;
- a uv lockfile for the current executable scaffold;
- Python 3.12+ support decision;
- typed runtime settings with an `.env.example` bootstrap;
- a foundation error model and FastAPI exception handler registration;
- structured JSON logging wired into the bootstrap path;
- `src/ddd_fast_api` layer packages for entrypoints, application, domain,
  infrastructure, and foundation;
- the first plain-Python catalog domain skeleton with invariant tests;
- the first application-layer catalog use case and repository port;
- a sample catalog HTTP endpoint wired through the application layer;
- a sample catalog detail endpoint with structured 400/404 responses;
- an initial architecture test that guards domain-layer imports;
- a minimal FastAPI app factory with `/` and `/health` routes;
- an initial unit test covering the scaffold entrypoints;
- a GitHub Actions quality workflow definition for tests, Ruff, and mypy;
- explicit Pydantic boundary schemas for the scaffold metadata endpoints;
- repository ignore rules;
- this project overview;
- MIT licensing.

Not yet present:

- business-domain implementation beyond the scaffold metadata endpoints;
- migrations, containers, Kubernetes manifests, or deployment workflows;
- comprehensive unit, integration, contract, architecture, and smoke tests.

## Getting started

The repository now contains a minimal executable foundation slice. It is not a
production service yet, but you can install the baseline dependencies, prepare
the initial environment file, run the app, and inspect the package layout that
future work will build on:

```bash
git clone https://github.com/owezzy/ddd-fast-api.git
cd ddd-fast-api
uv sync --group dev
cp .env.example .env
uv run python main.py
```

The local server starts on `http://127.0.0.1:8000` and currently exposes:

- `GET /` — scaffold metadata
- `GET /health` — simple health check
- `GET /catalog/items` — sample catalog items via the application layer
- `GET /catalog/items/{sku}` — one sample catalog item by SKU

Current runtime configuration lives in `src/ddd_fast_api/foundation/settings.py`
and is populated from `.env` using the `DDD_FAST_API_` prefix.

If you prefer stable task-style commands over raw uv invocations, the current
scaffold also provides:

```bash
make sync
make run
make test
make lint
make type-check
```

Read these sections next:

1. [Design principles](#design-principles) for the rules every contribution
   must preserve.
2. [Target architecture](#target-architecture) for layer responsibilities and
   dependency direction.
3. [Pydantic's role](#pydantics-role) for the boundary-versus-domain decision.
4. [Repository status](#repository-status) for an accurate implementation
   snapshot.
5. [Delivery roadmap](#delivery-roadmap) for the planned build sequence.

Development requirements for the current scaffold are:

- Git
- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

Python 3.12, 3.13, and 3.14 will be tested once CI is introduced. Docker,
Docker Compose, Kind, kubectl, and Kustomize become requirements in the
operations phase.

The root `main.py` is now a compatibility bootstrap that starts the packaged
application. It exists to keep the first runnable command simple while the
project transitions fully into the `src/ddd_fast_api` layout.

## Delivery roadmap

- [x] Define architecture, feature parity, and dependency rules.
- [x] Initialize and publish the repository.
- [x] Establish Python 3.12+ and MIT license decisions.
- [ ] **Foundation:** package layout, configuration, lifecycle, errors, logging,
      dependency rules, quality tools, and architecture tests.
- [ ] **Reference slice:** inventory/catalog contract, domain behavior,
      PostgreSQL adapter, migrations, and tests.
- [ ] **Production runtime:** account management, authentication,
      authorization, telemetry, health checks, and resilient HTTP clients.
- [ ] **Operations:** Docker, Compose, migration jobs, Kubernetes, CI/CD, and
      security scanning.
- [ ] **Template experience:** project generation, domain scaffolding,
      documentation, examples, and releases.
- [ ] **Validation:** generate a fresh service, run every workflow, deploy to
      local and Kubernetes environments, and complete a newcomer review.

## Contributing

The contribution workflow will be documented fully during the foundation
phase. Until then:

1. Open an issue describing the problem or proposed capability.
2. Keep changes focused and preserve the inward dependency rule.
3. Include tests and documentation with implemented behavior.
4. Submit changes through a pull request; do not merge feature work directly
   into `main`.

Architecture decisions that are expensive to reverse, surprising without
context, and based on a real trade-off should be recorded as ADRs.

## License

Distributed under the [MIT License](LICENSE).

## Acknowledgments

- [Ardan Labs Service](https://github.com/ardanlabs/service) for the production
  service architecture and operational-completeness inspiration.
- [FastAPI](https://fastapi.tiangolo.com/) and
  [Pydantic](https://docs.pydantic.dev/) for Python's typed API boundary tools.
- *Architecture Patterns with Python* by Harry Percival and Bob Gregory for
  practical ports, adapters, repositories, and units of work in Python.
