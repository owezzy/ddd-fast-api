# Domain-Oriented FastAPI Service Template

## Purpose

Create a production-grade, open-source FastAPI starter inspired by Ardan Labs Service. It is a starting point, not a framework: opinionated enough to remove setup guesswork, but simple enough for teams to change.

## Agreed Direction

- One deployable FastAPI service with modular domain boundaries.
- Pragmatic DDD: use tactical patterns only when the domain justifies them.
- Python 3.12 or newer, tested against Python 3.12, 3.13, and 3.14.
- PostgreSQL as the reference database.
- Docker Compose for local development and Kubernetes for production deployment.
- A small inventory/catalog reference domain with authenticated management.
- Local account signup and user management behind replaceable authentication ports, with external OIDC supported as an adapter.
- A generator that creates a consistent domain vertical slice.
- Minimal runtime dependencies and explicit wiring.
- MIT licensing for the public template.

## Architectural Pattern

Use domain-oriented ports and adapters with five memorable code layers:

1. **Entrypoints** — FastAPI routes, request and response schemas, CLI commands, startup, and shutdown.
2. **Application** — use cases, command/query orchestration, transaction boundaries, and authorization decisions.
3. **Domain** — entities, value objects, business rules, domain errors, events, and ports.
4. **Infrastructure** — PostgreSQL repositories, external clients, authentication adapters, and message adapters.
5. **Foundation** — small project-independent utilities for logging, telemetry, time, identifiers, and error metadata.

Domain modules are mirrored across the layers, so catalog code remains easy to trace from HTTP to storage. The composition root is the only place allowed to know every concrete implementation.

## Dependency Rules

- Entrypoints depend on Application and boundary models.
- Application depends on Domain ports and models.
- Domain imports neither FastAPI, Pydantic, SQLAlchemy, nor infrastructure.
- Infrastructure implements inward-facing ports and is selected only by the composition root.
- Foundation imports no project domain and remains independently reusable.
- Cross-domain work goes through explicit application interfaces, never direct repository access.
- Automated architecture tests enforce these import rules.

## Request and Transaction Flow

1. FastAPI validates transport input with Pydantic models.
2. A boundary mapper converts transport data into application input.
3. The application use case starts one explicit unit of work.
4. Domain behavior executes through ports.
5. Infrastructure repositories flush changes but never commit independently.
6. The application commits or rolls back the complete use case.
7. Domain results and errors are mapped to stable API responses.

Transactions belong to use cases, not generic HTTP middleware. This keeps retries, background jobs, and CLI operations consistent with HTTP behavior.

## Runtime and Platform Decisions

- FastAPI is an outer delivery adapter, not the application architecture.
- Application lifespan creates and closes shared resources such as database engines, telemetry providers, and HTTP clients.
- Request dependencies provide short-lived units of work and authenticated principals.
- Async is used for network and database I/O; CPU-heavy work is moved outside the event loop.
- Configuration uses validated environment settings with fail-fast startup checks.
- SQLAlchemy 2 async, asyncpg, and Alembic form the reference persistence stack.
- OpenAPI is treated as a tested public contract and versioned under a stable API prefix.

## Cross-Cutting Concerns

- Structured JSON logs with request, trace, actor, and operation identifiers.
- OpenTelemetry traces across HTTP, database, and outbound calls.
- Prometheus-compatible technical and business metrics.
- Separate liveness, readiness, and startup checks.
- Stable machine-readable error codes with safe public messages and internal causes.
- OIDC/JWT RS256 validation and policy-oriented authorization; no production signing keys in the repository.
- Timeouts, bounded retries, and idempotency for external side effects.

## Reference Domain

The inventory/catalog slice should demonstrate:

- Product identity and validated value objects.
- Stock adjustment rules and transactional consistency.
- Authenticated management with role-based policy examples.
- Filtering, ordering, and pagination.
- Domain errors mapped to API errors.
- Repository and unit-of-work ports with PostgreSQL adapters.
- Unit, integration, contract, and end-to-end tests.
- Business metrics and trace spans.

Keep authentication as platform capability rather than making identity the main business domain.

## Repository Capabilities

The public template should ship with:

- Locked dependencies and a single project configuration.
- Formatting, linting, strict type checking, security scanning, and pre-commit hooks.
- Multi-stage, non-root container builds.
- Docker Compose services for the API and PostgreSQL, with an optional observability profile.
- Alembic migration and deterministic seed commands.
- Kubernetes Kustomize base and environment overlays.
- A separate Kubernetes migration Job to avoid replica startup races.
- Resource requests and limits, probes, graceful termination, and disruption settings.
- GitHub Actions for lint, type check, tests, migration validation, image build, vulnerability scan, and release.
- Architecture documentation, decision records, contribution guide, changelog, and security policy.

## Testing Strategy

- Domain and application tests run without FastAPI or a database.
- Repository integration tests use real PostgreSQL through containers.
- API tests verify routing, authentication, error mapping, and OpenAPI behavior.
- Contract and property-based tests exercise the generated OpenAPI schema.
- Architecture tests reject forbidden imports and ORM leakage.
- Migration tests verify upgrade from an empty database and the previous released schema.
- A small smoke suite runs against Docker Compose and Kubernetes.

## Domain Generator

The generator should create only consistent seams: domain module, application use cases, ports, transport adapter, persistence adapter, tests, and registration hooks. Generated code must be immediately testable and removable. It must not invent business rules or force aggregates where simple domain services are sufficient.

## Delivery Phases

1. **Foundation** — repository layout, dependency rules, configuration, logging, errors, lifecycle, and quality tooling.
2. **Reference slice** — catalog domain from API contract through PostgreSQL with tests.
3. **Production runtime** — authentication, authorization, telemetry, health checks, and resilient outbound clients.
4. **Operations** — containers, Compose, migrations, Kubernetes, CI, and security scanning.
5. **Template experience** — domain generator, naming customization, documentation, examples, and release automation.
6. **Validation** — generate a fresh project, run all workflows, deploy locally and to Kubernetes, and review from a new contributor's perspective.

## Success Criteria

- A new contributor can run the stack and tests with one documented command.
- Business rules can be tested without FastAPI, SQLAlchemy, PostgreSQL, or network access.
- Layer violations fail CI.
- Local and Kubernetes behavior use the same configuration and migration model.
- The template exposes useful logs, metrics, traces, and health signals by default.
- A generated domain follows the same architecture as the reference domain.
- Removing the sample domain leaves a valid, documented starter.

## Explicit Non-Goals

- A FastAPI replacement or general-purpose framework.
- Mandatory event sourcing, CQRS, message brokers, caching, or service mesh.
- Multiple deployable microservices in the initial template.
- Abstract repositories for trivial read-only queries without a business boundary.
- Cloud-provider-specific deployment as the only supported path.

## Ardan Feature-Parity Matrix

All listed Ardan capabilities have a viable Python implementation. The classifications below describe conceptual parity, not current implementation status: this repository is still a plan and the template must be built through the delivery phases above.

### Direct Equivalents

- **Ground-up Kubernetes architecture** — container-first FastAPI runtime, Kubernetes Deployments and Services, Kustomize base and overlays, probes, resource policies, and graceful termination.
- **API protocol and business separation** — FastAPI and Pydantic remain in Entrypoints; Application and Domain stay transport-independent.
- **Local and production Kubernetes environments** — Docker Compose is the default local workflow; local Kubernetes can use Kind and Tilt, while Kustomize overlays define development, staging, and production.
- **Minimal web-service framework** — FastAPI and Starlette provide routing, validation, lifecycle, exception handling, and OpenAPI; project conventions add architecture without wrapping FastAPI in another framework.
- **Middleware integration** — Starlette middleware handles transport-wide concerns; FastAPI dependencies handle route and identity concerns; application decorators handle business telemetry and policy concerns.
- **PostgreSQL support** — PostgreSQL with SQLAlchemy 2 async, asyncpg, explicit repository ports, units of work, and Alembic migrations.
- **CRUD pattern** — thin routes, application use cases, domain rules, repository adapters, stable errors, and explicit list filtering, ordering, and pagination.
- **RBAC** — validated OIDC/JWT claims mapped to an authenticated principal, with route-level permission dependencies and object-level policy checks in Application. Open Policy Agent remains an optional adapter for centralized policy.
- **Account signup and user management** — a dedicated identity capability for password hashing or external OIDC, account lifecycle, role assignment, token validation, and audit events. Authentication remains separate from the inventory business domain.
- **Distributed logging and tracing** — structured standard-library logging with correlation and trace identifiers plus OpenTelemetry context propagation.
- **OpenTelemetry observability** — OpenTelemetry SDK and instrumentation for FastAPI, SQLAlchemy, and outbound HTTP, exported through an OpenTelemetry Collector.
- **Testing patterns** — pytest, pytest-asyncio, HTTPX, Testcontainers for PostgreSQL, contract tests, property-based tests, architecture tests, and deployment smoke tests.
- **Docker, Docker Compose, and Makefiles** — multi-stage non-root image, Compose development stack, and a Makefile or equivalent task runner exposing stable project commands.
- **Continuous deployment pipeline** — CI quality and security gates followed by image publication, migration validation, environment deployment, smoke testing, and promotion.
- **CircleCI integration** — CircleCI can implement the pipeline directly. GitHub Actions is the recommended default for a GitHub template, with CircleCI maintained as an optional example rather than a second required pipeline.
- **Tempo and Grafana** — use the same products with an OpenTelemetry Collector; Compose provides an optional local profile and Kubernetes provides maintained observability manifests or documented external endpoints.

### Adapted Equivalents

- **Domain Driven, Data Oriented Design** — pragmatic DDD maps directly; Go-specific data-layout and value/pointer choices become explicit Python domain models, immutable value objects, boundary DTOs, controlled mutation, and profiling-based optimization. This is an architectural discipline, not a package dependency.
- **Vendoring dependencies with Modules** — Python should not commit installed packages into the source tree. Use `pyproject.toml` plus `uv.lock`, frozen synchronization, hashes, and dependency scanning for reproducibility. For air-gapped builds, publish or build a wheelhouse and install only from that approved artifact source. Literal source vendoring is reserved for patched dependencies with documented provenance.
- **Documentation generated by reading code** — FastAPI generates OpenAPI from routes and boundary schemas; MkDocs with mkdocstrings generates source API references from typed public interfaces and docstrings. Architecture rationale, domain language, operations, and ADRs remain curated because code alone cannot explain intent.
- **Code generation for each new domain** — a Copier-backed project template and a small domain-scaffolding CLI generate mirrored Domain, Application, Entrypoint, Infrastructure, test, and registration seams. Generation creates structure only; it never invents business rules. Generated output must pass formatting, typing, architecture, and tests immediately.

### Parity Acceptance Rule

A feature counts as implemented only when it has source code or configuration, automated tests, user documentation, and a passing CI check. A dependency choice or plan entry alone does not count as implementation.
