# e-commerce-microservices


## Presentation videos 
[Youtube playlist](https://youtu.be/FpN1-x2qDtk?feature=shared)

## Introduction

The aim of this project was to develop a distributed microservice system designed to facilitate fundamental shop functionalities like: listing/adding products, listing/adding orders, user registering/logging-in. The system consists of microservice applications that collaborate by transmitting events through the message broker. Due to its distributed nature of functionalities  the system demonstrates resilience to a certain extent. In case of failure it consumes lacking events from the broker and makes the databases consistent. In the case of failure of microservices, it retrieves missing events from the broker and ensures the consistency of databases.

Database credentials: admin / pass
App admin credentials: admin@admin.com / admin@admin.com
App user credentials: aaa@aaa.com / aaa@aaa.com

## System architecture

The system consists of a reverse proxy that serves the frontend application and passes API requests from frontend to backend. The backend consists of 4 microservices: gateway-ms, authentication-ms, products-ms, orders-ms. There are 3 document databases for each of the microservices except for gateway-ms which has some in-code data embedded. Message broker is used by two of the microservices products-ms and orders-ms in order to keep the state of orders consistent.

![image](https://github.com/heyimjustalex/e-commerce-microservices/assets/21158649/f4a80acf-527e-469e-bba9-105bf09f195f)

## Backend architecture

All of the services are developed with REST API Python Framework FastAPI. Each of the services have different purposes and therefore, conceptually separated functionalities. Three of the microservices use separate document databases and two of these keep data consistent by using events and brokers.

![image](https://github.com/heyimjustalex/e-commerce-microservices/assets/21158649/39ebe49e-b908-4042-a2d7-4702795a3ea8)


### Microservices
Backend system consists of:

**gateway-ms** - Microservice responsible for passing the request to relevant microservice (based on requested path) and for authorization of users based on the token that user attaches to the requests. JWT token is decoded by the microservice and verified using private secret. Based on the role and  the endpoint that the user tries to access (HTTP_VERB and PATH) the decision is made regarding passing the access or returning relevant HTTP_CODE. 

**authentication-ms** - Microservice responsible for registering and logging-in users by providing JWT authentication. There is also a refresh functionality to renew an access token by using refresh token. User credentials (email and password) and roles (user or admin) are saved in the document database.

**products-ms** - Microservice responsible for listing the products, getting single product by name or multiple by category. Administrator of the shop is also able to add a new product. This microservice is able to generate/consume relevant events: ProductCreateEvent, OrderCreateEvent, OrderStatusUpdateEvent, ProductsQuantityUpdateEvent. It checks whether the event has already been consumed in order to avoid any duplicates and inconsistencies in the database.

**orders-ms**- Microservice responsible for listing the orders and accepting a new order.  This microservice is able to generate/consume relevant events: ProductCreateEvent, OrderCreateEvent, OrderStatusUpdateEvent, ProductsQuantityUpdateEvent.  It also checks whether the event has already been consumed in order to avoid any duplicates and inconsistencies in the database.

### Layered architecture of each service
All of the microservices except for gateway-ms have a layered structure with 3 main layers: controller, service and repository. Abstraction helps to separate endpoints definition, business logic and data manipulation functionalities.

### Event Handling

Two of the microservices - products-ms and orders-ms communicate through the Kafka message broker by producing and consuming relevant events. Event model classes are serialized by one service and deserialized by the other one. In order to make the system consistent both of the microservices use local transactions to save data in local databases and at the same time publish it to the broker. If either of these operations fail, the whole transaction fails.

### Containerization
Each of the backend microservices is containerized with Docker. Services have Dockerfile and Dockerfile.prod versions of Dockerfile and they differ with package requirements that are embedded in Docker image and stages (production includes stage of testing). For development purposes docker-compose is used with hot-reload of the code and bind mounts.

### Tests

Three of the microservices (orders-ms, products-ms and authentication-ms) are tested with pytest and mongomock. The DB that is used by endpoints is MongoMock which is an in-memory database, so the whole testing process might be performed in a single container and not a specialized environment (get_db function mocked).


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

### Deploy with GKE

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
helm install my-ing ingress-nginx/ingress-nginx --namespace ingress --version 4.0.17 --values .\infrastructure\kubernetes\gcp\nginx-values.yaml --create-namespace
```

```
./build-all-images-dockerhub.ps1
```

```
./deploy-gcp-k8s.ps1
```

Get external IP and change your DNS:

```
kubectl get services -n ingress
```

![image](https://github.com/heyimjustalex/e-commerce-microservices/assets/21158649/e261c7ff-3ef1-4aa4-8ed5-ce2c21dd899e)


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

## K8S debug commands

```
kubectl get pods
```

```
kubectl get pods -n ingress
```

```
kubectl get services
```

```
kubectl get services -n ingress
```

```
kubectl logs <pod-id>
```

```
kubectl describe pod
```

