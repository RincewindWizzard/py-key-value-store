#!/bin/bash
VERSION=$(cat pyproject.toml | grep version | sed 's/^version = "\(.*\)"$/\1/g')  #-$(printf %x "$(date +%s)")
#DOCKER_REPO="rincewindwizzard/key-value-store"

# replace with docker if needed
PODMAN=podman

echo "Building version v$VERSION"
echo "Docker Image: $DOCKER_REPO:$VERSION"

# Build docker image
$PODMAN build -t "$DOCKER_REPO:latest" -t "$DOCKER_REPO:$VERSION" .

$PODMAN push "$DOCKER_REPO:latest"
$PODMAN push "$DOCKER_REPO:$VERSION"

# create helm chart
mkdir helm 2> /dev/null
$PODMAN run -v "$(pwd)/helm/:/app/helm/" -ti "$DOCKER_REPO:$VERSION" python3 helm.py

# install helm chart
helm upgrade --install key-value-store --values helm/values.yaml helm #--dry-run

# deploy a debug shell container
# kubectl run debug-shell --rm -i --tty --image ubuntu -- bash
