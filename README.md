# Example Python Application on Kubernetes

Uses:

- flask
- poetry
- podman
- helm
- kubernetes

## Prerequisites

- docker
- helm
- kubectl

You have to configure kubectl to have access to the cluster and default namespace.
Your podman client has to be logged into the docker registry:

    docker login docker.io

And you have to set DOCKER_REPO to your docker hub repository.

    DOCKER_REPO="rincewindwizzard/key-value-store" ./build.sh

If successful this application runs on your cluster.

    $ kubectl get pods
    NAME                                  READY   STATUS    RESTARTS   AGE
    py-key-value-store-86cc69c47b-pmlpf   1/1     Running   0          11s

## Examples

Put a value:

    curl -X PUT http://<KUBERNETES>/py-key-value-store/doc/hallo -d '{"foo": "ich war hier"}' -H 'Content-Type: application/json'

Retrieve value:

    curl http://<KUBERNETES>/py-key-value-store/doc/hallo

List all keys:

    curl http://<KUBERNETES>/py-key-value-store/doc/

Get health and ENV:

    curl http://<KUBERNETES>/py-key-value-store/health

Running a fresh ubuntu install for debugging purposes in the cluster:

    kubectl run debug-shell --rm -i --tty --image ubuntu -- bash