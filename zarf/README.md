# Operations package

All container and deployment assets live under `zarf/`.

## Local Compose

```bash
docker compose -f zarf/compose/docker-compose.yml up --build
docker compose -f zarf/compose/docker-compose.yml down -v
```

Compose starts PostgreSQL, runs `alembic upgrade head` in the `migrate`
service, and only then starts the API. The API never runs migrations during
application startup. PostgreSQL is exposed on host port `15432` by default;
set `POSTGRES_HOST_PORT=5432` when that port is available. The API is exposed
on host port `8000` by default; set `API_HOST_PORT=18000` when that port is
already in use.

## Local Kind cluster

The `zarf/k8s/dev` tooling mirrors the current Ardan Labs Kind pattern:

```bash
make dev-run
```

This creates a Kind cluster with a local registry at `localhost:5001`, builds
and pushes the development image, provisions PostgreSQL, runs the migration
Job, and deploys the API. The command names follow the Ardan Labs development
workflow: use `make dev-up-registry`, `make dev-load`, and `make dev-apply`
individually when iterating.

The development workflow also installs ingress-nginx and exposes the API at
`http://ddd-fast-api.localhost:8000`. Verify it with:

```bash
curl --fail -H 'Host: ddd-fast-api.localhost' \
	 http://127.0.0.1:8000/health/ready
```

## Kustomize

Render the portable base and overlays with the Kubernetes CLI:

```bash
kubectl kustomize zarf/k8s/base
kubectl kustomize zarf/k8s/overlays/development
kubectl kustomize zarf/k8s/overlays/production
```

Each overlay includes the namespace, ConfigMap, API Deployment, Service, and a
separate migration Job. The migration Job is intentionally not part of API
startup. For strict migration-before-rollout ordering, use the Helm chart,
whose `pre-install,pre-upgrade` hook waits for the migration Job before Helm
promotes the release.

## Helm

Render the chart without a cluster:

```bash
helm lint zarf/chart
helm template ddd-fast-api zarf/chart -n ddd-fast-api
helm template ddd-fast-api zarf/chart -n ddd-fast-api \
  -f zarf/chart/values-production.yaml
```

Create the external secret before installing:

```bash
kubectl apply -f zarf/secret.example.yaml
helm upgrade --install ddd-fast-api zarf/chart \
  --namespace ddd-fast-api --create-namespace \
  -f zarf/chart/values-production.yaml
```

The migration Job is a Helm `pre-install,pre-upgrade` hook. This keeps schema
changes separate from application pod startup and makes migrations run once
before a release is promoted.

## Operations directory

The `zarf/` directory is only the repository's operations-assets directory. It
does not require the Zarf packaging tool. The supported deployment surfaces are
Docker Compose, Helm, Kustomize, and the local Kind bootstrap.
