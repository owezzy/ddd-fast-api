#!/bin/sh
set -eu

cluster_name="${KIND_CLUSTER_NAME:-ddd-fast-api}"
node_image="${KIND_NODE_IMAGE:-kindest/node:v1.35.0}"
registry_name="${KIND_REGISTRY_NAME:-kind-registry}"
registry_port="${KIND_REGISTRY_PORT:-5001}"
kind_network="kind"

if [ "$(docker inspect -f '{{.State.Running}}' "${registry_name}" 2>/dev/null || true)" != "true" ]; then
  docker run -d --restart=always \
    -p "127.0.0.1:${registry_port}:5000" \
    --network bridge --name "${registry_name}" registry:2
fi

if ! kind get clusters | grep -qx "${cluster_name}"; then
  kind create cluster --image "${node_image}" \
    --config zarf/k8s/dev/kind-config.yaml --name "${cluster_name}"
fi

kubectl config use-context "kind-${cluster_name}"

registry_dir="/etc/containerd/certs.d/localhost:${registry_port}"
for node in $(kind get nodes --name "${cluster_name}"); do
  docker exec "${node}" mkdir -p "${registry_dir}"
  printf '[host."http://%s:5000"]\n' "${registry_name}" \
    | docker exec -i "${node}" cp /dev/stdin "${registry_dir}/hosts.toml"
done

if ! docker network inspect "${kind_network}" \
  --format '{{range .Containers}}{{.Name}}{{"\n"}}{{end}}' \
  | grep -qx "${registry_name}"; then
  docker network connect "${kind_network}" "${registry_name}"
fi

kubectl --context="kind-${cluster_name}" apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: local-registry-hosting
  namespace: kube-public
data:
  localRegistryHosting.v1: |
    host: "localhost:${registry_port}"
    help: "https://kind.sigs.k8s.io/docs/user/local-registry/"
EOF

printf '%s\n' "Kind cluster ${cluster_name} is ready; registry is localhost:${registry_port}."
