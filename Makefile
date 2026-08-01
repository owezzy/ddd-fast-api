KIND            := kindest/node:v1.35.0
KIND_CLUSTER    := ddd-fast-api-cluster
KIND_CONTEXT    := kind-$(KIND_CLUSTER)
NAMESPACE       := ddd-fast-api
BASE_IMAGE_NAME := localhost:5001
APP_IMAGE       := $(BASE_IMAGE_NAME)/ddd-fast-api
VERSION         := dev
API_PORT        := 18001
KUBECTL         := kubectl --context=$(KIND_CONTEXT)

.PHONY: help sync run test lint format type-check hooks commit clean \
	compose-up compose-down docker-build helm-lint helm-template kustomize-dev \
	kustomize-prod kustomize-database dev-up dev-down dev-up-registry \
	dev-down-registry dev-ingress dev-load dev-apply dev-run dev-update \
	dev-update-apply dev-status-all dev-status dev-logs dev-logs-db \
	dev-describe-deployment dev-describe-database dev-events dev-forward

help:
	@printf "Available targets:\n"
	@printf "  sync        Install runtime and development dependencies via uv\n"
	@printf "  run         Start the current scaffold application\n"
	@printf "  test        Run pytest\n"
	@printf "  lint        Run Ruff checks\n"
	@printf "  format      Apply Ruff fixes and formatting\n"
	@printf "  type-check  Run mypy against src\n"
	@printf "  hooks       Install local Husky git hooks\n"
	@printf "  commit      Open an interactive Commitizen conventional commit prompt\n"
	@printf "  clean       Remove local caches and test artifacts\n"
	@printf "  compose-up  Start PostgreSQL, migrations, and API with Compose\n"
	@printf "  compose-down Stop the Compose stack and volumes\n"
	@printf "  docker-build Build the production image\n"
	@printf "  helm-lint   Validate the deployment Helm chart\n"
	@printf "  helm-template Render the deployment Helm chart\n"
	@printf "  kustomize-dev Render the development Kustomize overlay\n"
	@printf "  kustomize-prod Render the production Kustomize overlay\n"
	@printf "  kustomize-database Render the Kind PostgreSQL component\n"
	@printf "  dev-up     Create a local Kind cluster\n"
	@printf "  dev-down   Delete the local Kind cluster\n"
	@printf "  dev-up-registry Create Kind with the local image registry\n"
	@printf "  dev-down-registry Delete Kind and the local image registry\n"
	@printf "  dev-ingress Install the local ingress-nginx controller\n"
	@printf "  dev-load   Build and push the development image\n"
	@printf "  dev-apply  Provision PostgreSQL and apply the application\n"
	@printf "  dev-run    Create, build, provision, and deploy the local stack\n"
	@printf "  dev-update Build and restart the running API\n"
	@printf "  dev-update-apply Build and reapply the full local stack\n"
	@printf "  dev-status-all Show nodes, services, and pods\n"
	@printf "  dev-status Watch all Kubernetes pods\n"
	@printf "  dev-logs   Tail API logs\n"
	@printf "  dev-logs-db Tail PostgreSQL logs\n"
	@printf "  dev-describe-deployment Describe the API deployment\n"
	@printf "  dev-describe-database Describe the PostgreSQL pod\n"
	@printf "  dev-events Show namespace events\n"
	@printf "  dev-forward Forward the API service to localhost\n"

sync:
	uv sync --group dev

run:
	uv run python main.py

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff check . --fix
	uv run ruff format .

type-check:
	uv run mypy src

hooks:
	npm install
	git config core.editor "uv run cz commit --dry-run --write-message-to-file"

commit:
	uv run cz commit

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov build dist
	rm -f .coverage coverage.xml

compose-up:
	docker compose -f zarf/compose/docker-compose.yml up --build

compose-down:
	docker compose -f zarf/compose/docker-compose.yml down -v

docker-build:
	docker build -f zarf/Dockerfile -t ddd-fast-api:local .

helm-lint:
	helm lint zarf/chart

helm-template:
	helm template ddd-fast-api zarf/chart --namespace ddd-fast-api

kustomize-dev:
	kubectl kustomize zarf/k8s/overlays/development

kustomize-prod:
	kubectl kustomize zarf/k8s/overlays/production

kustomize-database:
	kubectl kustomize zarf/k8s/dev/database

dev-up:
	kind create cluster --image $(KIND) --name $(KIND_CLUSTER) \
		--config zarf/k8s/dev/kind-config.yaml
	kubectl config use-context $(KIND_CONTEXT)

dev-down:
	kind delete cluster --name $(KIND_CLUSTER)

dev-up-registry:
	KIND_CLUSTER_NAME=$(KIND_CLUSTER) KIND_NODE_IMAGE=$(KIND) \
		sh zarf/k8s/dev/kind-with-registry.sh

dev-down-registry:
	kind delete cluster --name $(KIND_CLUSTER) 2>/dev/null || true
	docker stop kind-registry 2>/dev/null || true
	docker rm kind-registry 2>/dev/null || true

dev-ingress:
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx \
		--force-update
	helm repo update ingress-nginx
	helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
		--namespace ingress-nginx --create-namespace \
		--set controller.hostPort.enabled=true \
		--set controller.hostPort.ports.http=8000 \
		--set controller.hostPort.ports.https=8443 \
		--set controller.service.type=NodePort
	$(KUBECTL) wait --namespace=ingress-nginx \
		--for=condition=available deployment/ingress-nginx-controller \
		--timeout=180s

dev-load:
	docker build -f zarf/Dockerfile -t $(APP_IMAGE):$(VERSION) .
	docker push $(APP_IMAGE):$(VERSION)

dev-apply:
	$(KUBECTL) apply -k zarf/k8s/dev/database
	$(KUBECTL) rollout status --namespace=$(NAMESPACE) --watch --timeout=180s \
		statefulset/ddd-fast-api-postgres
	$(KUBECTL) delete job ddd-fast-api-migration --namespace=$(NAMESPACE) \
		--ignore-not-found
	$(KUBECTL) apply -k zarf/k8s/overlays/development
	$(KUBECTL) wait --for=condition=complete job/ddd-fast-api-migration \
		--namespace=$(NAMESPACE) --timeout=240s
	$(KUBECTL) rollout status deployment/ddd-fast-api \
		--namespace=$(NAMESPACE) --timeout=240s

dev-run:
	$(MAKE) dev-up-registry
	$(MAKE) dev-ingress
	$(MAKE) dev-load
	$(MAKE) dev-apply

dev-update:
	$(MAKE) dev-load
	$(KUBECTL) rollout restart deployment/ddd-fast-api --namespace=$(NAMESPACE)
	$(KUBECTL) rollout status deployment/ddd-fast-api --namespace=$(NAMESPACE) \
		--timeout=240s

dev-update-apply:
	$(MAKE) dev-load
	$(MAKE) dev-apply

dev-status-all:
	$(KUBECTL) get nodes -o wide
	$(KUBECTL) get svc -o wide --namespace=$(NAMESPACE)
	$(KUBECTL) get pods -o wide --namespace=$(NAMESPACE)

dev-status:
	$(KUBECTL) get pods --all-namespaces --watch

dev-logs:
	$(KUBECTL) logs --namespace=$(NAMESPACE) \
		-l app.kubernetes.io/name=ddd-fast-api --all-containers=true \
		-f --tail=100

dev-logs-db:
	$(KUBECTL) logs --namespace=$(NAMESPACE) \
		statefulset/ddd-fast-api-postgres --all-containers=true -f --tail=100

dev-describe-deployment:
	$(KUBECTL) describe deployment --namespace=$(NAMESPACE) ddd-fast-api

dev-describe-database:
	$(KUBECTL) describe pod --namespace=$(NAMESPACE) \
		-l app.kubernetes.io/name=ddd-fast-api-postgres

dev-events:
	$(KUBECTL) get events --namespace=$(NAMESPACE) --sort-by=.lastTimestamp

dev-forward:
	$(KUBECTL) port-forward --namespace=$(NAMESPACE) service/ddd-fast-api \
		$(API_PORT):80
