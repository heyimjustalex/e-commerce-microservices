# e-commerce-microservices

## Deploy with GKE

### Generate Let's Encrypt certificate

```
apt install certbot python3-certbot-nginx
```

```
certbot -d cloudcomputingtechnologies.pl --manual --preferred-challenges dns certonly
```

```
cat /etc/letsencrypt/live/cloudcomputingtechnologies.pl/fullchain.pem
```

```
cat /etc/letsencrypt/live/cloudcomputingtechnologies.pl/privkey.pem
```

Paste certifiate (only one, not fullchain and priv key to ingress.yaml)

### Deploy infrastructure

```
gcloud auth application-default login
```

```
cd ./infrastructure/terraform

```

```
terraform init
```

```
terraform apply
```

```
gcloud container clusters get-credentials primary --zone europe-north1-a --project <project_name_login.json>
```

Here you get connection string:

![image](https://github.com/heyimjustalex/e-commerce-microservices/assets/21158649/898cebe7-123f-4772-bd11-ef4681d1f45b)



Connect to the cluster

### GKE operations

```
kubectl config get-contexts
```

```
kubectl config set current-context <context-name>
```

```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
```

```
helm repo update
```

```
helm install my-ing ingress-nginx/ingress-nginx --namespace ingress --version 4.0.17 --values .\infrastructure\kubernetes\nginx-values.yaml --create-namespace
```

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
./build-all-images-docker.ps1
```

```
./deploy-minikube.ps1
```

```
kubectl port-forward svc/nginx-proxy-svc 80:80
```

## Deploy with Docker (Development)

```
docker-compose -f docker-compose-dev.yaml up --build
```

## Deploy with Docker (Production)

```
docker-compose -f docker-compose-prod.yaml up --build
```
