#!/bin/bash
VERSION=$(cat pyproject.toml | grep version | sed 's/^version = "\(.*\)"$/\1/g')


echo "Building version v$VERSION"

# Build docker image
podman build -t "rincewindwizzard/key-value-store:latest" -t "rincewindwizzard/key-value-store:$VERSION" .

podman push "rincewindwizzard/key-value-store:latest"
podman push "rincewindwizzard/key-value-store:$VERSION"

poetry run helm

helm upgrade --install key-value-store --values helm/values.yaml helm #--dry-run

# deploy a debug shell container
# kubectl run debug-shell --rm -i --tty --image ubuntu -- bash
