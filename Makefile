#VERSION = $(eval cat pyproject.toml | grep version | sed 's/^version = "\(.*\)"$/\1/g')
VERSION = Hallo
echo-version:
	echo "$(VERSION)"
	cat pyproject.toml | grep version | sed 's/^version = "\(.*\)"$/\1/g'

docker:
	podman build -t rincewindwizzard/key-value-store:latest -t rincewindwizzard/key-value-store:$(VERSION) .
	podman push rincewindwizzard/key-value-store:latest

run:
	podman run -p 8000:8000 -ti localhost/py-key-value-store

helm-install:
	helm upgrade key-value-store ./helm/

# deploy a debug shell container
# kubectl run debug-shell --rm -i --tty --image ubuntu -- bash
#helm upgrade --install <release name> --values <values file> <chart directory>