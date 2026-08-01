# End-to-End Validation

This validation path is designed for a fresh clone. Run commands from the
repository root.

## Fresh-clone quality checks

```bash
uv sync --group dev
make test
make lint
make type-check
```

Expected results:

- pytest passes all tests;
- Ruff reports no findings;
- mypy reports no issues.

## Live application smoke check

Copy `.env.example` to `.env`, then start the application:

```bash
cp .env.example .env
uv run python main.py
```

In another terminal, verify the public runtime surface:

```bash
curl --fail http://127.0.0.1:8000/health/live
curl --fail http://127.0.0.1:8000/health/ready
curl --fail http://127.0.0.1:8000/
curl --fail http://127.0.0.1:8000/metrics
```

The application uses in-memory adapters by default, so this smoke check does
not require PostgreSQL.

## Compose database and migration path

```bash
make compose-up
```

If host port `8000` is already in use, run the stack on an alternate API port:

```bash
API_HOST_PORT=18000 make compose-up
```

Use the same port in the smoke-check URLs.

Compose starts the PostgreSQL `database` service, waits for its healthcheck,
runs the separate Alembic `migrate` service, and then starts the API. Stop the
stack with:

```bash
make compose-down
```

The Compose `pg_hba.conf` is development-only. Production deployments must
provide managed credentials and an environment-specific PostgreSQL access
policy.

## Kubernetes packaging checks

```bash
make helm-lint
make helm-template
make kustomize-dev
make kustomize-prod
make kustomize-database
```

## Local Kind deployment

Requirements: Docker, Kind, kubectl, and a running Docker daemon.

```bash
make dev-run
make dev-status-all
```

The Kind workflow creates the local registry, builds and pushes the API image,
installs ingress-nginx, provisions PostgreSQL, runs the migration Job, and waits
for the API rollout. Verify the Ingress route with:

```bash
curl --fail -H 'Host: ddd-fast-api.localhost' \
	 http://127.0.0.1:8000/health/ready
```

Use `make dev-update` for application-only changes and
`make dev-update-apply` when manifests or migrations changed. `make
dev-forward` remains available as a temporary service-level fallback.

## CI coverage

`.github/workflows/quality.yml` runs the quality matrix on Python 3.12, 3.13,
and 3.14, audits dependencies, scans the repository, validates Compose, builds
the production image, and renders the Helm and Kustomize resources.

The dedicated contract and full end-to-end smoke test suites remain future
work; the current validation is automated where practical and explicitly
documents the local checks that require Docker, Kubernetes, or a live process.
