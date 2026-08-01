# Local Kind cluster

This follows the local-registry workflow used by the current Ardan Labs service
repository. It creates a Kind control-plane cluster, starts a local OCI
registry, configures containerd to resolve `localhost:5001` from inside the
cluster, and publishes the registry location through `kube-public`.

Requirements: Docker, Kind, and kubectl.

```bash
make dev-run
```

This installs the local `ingress-nginx` controller and routes
`http://ddd-fast-api.localhost:8000` to the API. The `ddd-fast-api.localhost`
hostname resolves to loopback in modern browsers and curl; use an explicit
`Host` header if your environment does not resolve it:

```bash
curl --fail -H 'Host: ddd-fast-api.localhost' \
	 http://127.0.0.1:8000/health/ready
```

Useful follow-up commands:

```bash
make dev-status-all
make dev-logs
make dev-forward
```

`make dev-forward` remains available as a temporary service-level fallback and
exposes the API at `http://127.0.0.1:18001` by default.
Override the local port with `make dev-forward API_PORT=8001`.

Use `make dev-update` after changing application code, or
`make dev-update-apply` when Kubernetes manifests or migrations changed. Use
`make dev-down-registry` to remove both the Kind cluster and its local registry.

The Kustomize application overlay creates local-only development credentials.
For a Helm install instead, create the external application secret and install
the chart using the commands in `zarf/README.md`.

The `dev-*` Make targets bind Kubernetes operations to the configured Kind
context. If running `kubectl` directly, select that same context first:

```bash
kubectl config use-context kind-ddd-fast-api-cluster
```

The Kind database component follows Ardan's dedicated database pattern: a
PostgreSQL 18 StatefulSet, a persistent volume claim, a ClusterIP service, and
readiness/liveness probes. The Helm chart's migration hook runs before the API
deployment. For Kustomize, apply the database component and wait for it before
applying the application overlay; production should use an externally managed
PostgreSQL service and externally managed secrets.
