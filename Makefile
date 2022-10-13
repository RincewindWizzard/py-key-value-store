docker:
	podman build -t py-key-value-store .

run:
	podman run -p 8000:8000 -ti localhost/py-key-value-store

helm-install:
	helm install key-value-store ./helm/