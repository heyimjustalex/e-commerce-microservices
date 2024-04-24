# e-commerce-microservices

## Deploy with Minikube

```
docker context use default
```

```
minikube start --driver=docker
```

```
kubectl config get-contexts
```

```
kubectl config set current-context minikube
```

```
./build-all-images-docker.ps1/sh
```

```
./deploy-minikube.ps1/sh
```

```
kubectl port-forward svc/nginx-proxy-svc 80:80
```

## Deploy with Docker (Development)

docker-compose -f docker-compose-dev.yaml up --build

## Deploy with Docker (Production)

docker-compose -f docker-compose-prod.yaml up --build
