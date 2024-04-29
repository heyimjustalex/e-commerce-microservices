# e-commerce-microservices


## Presentation videos 
[Youtube playlist](https://youtu.be/FpN1-x2qDtk?feature=shared)

## Detailed description available in report.pdf file

## Introduction

The aim of this project was to develop a distributed microservice system designed to facilitate fundamental shop functionalities like: listing/adding products, listing/adding orders, user registering/logging-in. The system consists of microservice applications that collaborate by transmitting events through the message broker. Due to its distributed nature of functionalities  the system demonstrates resilience to a certain extent. In case of failure it consumes lacking events from the broker and makes the databases consistent. In the case of failure of microservices, it retrieves missing events from the broker and ensures the consistency of databases.

**Database credentials:** admin / pass <br/>
**App admin credentials:** admin@admin.com / admin@admin.com <br/>
**App user credentials**: aaa@aaa.com / aaa@aaa.com <br/>

## Non-functional requirements

According to the first report I have chosen availability/resiliency and security requirements. Availability/resiliency is achieved by designing microservices in a stateless way and changing the number of replicas in the configuration of K8S deployment.



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

### Databases

There are 3 distributed databases in the system. Each of them is a Bitnami MongoDB document database that supports transactions. All of them have different schemas, but the schema creation and the initialization of data is done in the same way with Docker and the db/init.js file for each of them.  Schemas for each of the microservices:

#### authentication-db
Inside authentication-db there is a ‘shop’ document database and inside of it there is a collection ‘users’. Each record in the collection has 4 attributes _id, email, role password_hash. Email is used as username and Role may be user or admin and hashing algorithm SHA-256 is used for the password transformation.

#### products-db 
There is a ‘shop’ document database and inside there are collections ‘orders’, ‘products’, ‘categories’. Each record in the ‘products’ collection has 6 attributes _id, name, description, price, quantity, categories. Categories is an array of _id from categories collection. The ‘categories’ collection has _id and name attributes. Ids are bound to product records and we are able to see the name of the category when listing products from the backend.
<br/>
Orders stub collection has information about which of the events have been already consumed by products-ms. If there is OrderCreateEvent sent from orders-ms then products-ms consumes the event, save status as ACCEPTED if there is enough quantity for the products. Then responds with another event about the product's quantity change.

#### orders-db 
Inside orders-db there is a ‘shop’ document database and inside there are collections ‘orders’, ‘products’ that are responsible for order data handling. Each record in the ‘orders’ collection has 4 attributes _id, client_email, status, cost, products. The contents of the product collections are stub versions of products embedded in the order record. Each record in the ‘orders’ collection has 4 attributes: name, price, quantity. This collection is only to make an initial decision about the sale of products. If orders-ms does not have required product quantity i reject the user request and does not try to generate events. If the quantity of bought products in the local products collection is available, it creates an OrderCreate event and the order in the ‘orders’ collection in the pending state. If products-ms is available it can either accept or reject the order.

### Events

Microservices products-ms and orders-ms produce events in order to keep their databases consistent. Available event types are listed as models in the code in both of the applications. 

#### ProductCreateEvent
This event is generated when the administrator of the shop adds a new product to the inventory, and products need to be populated into both of the ‘products’ collections in ‘orders-db’ and ‘products-db’.

![image](https://github.com/heyimjustalex/e-commerce-microservices/assets/21158649/c0ca68f3-70b4-48c3-bbdf-a956ff3f0aed)
![image](https://github.com/heyimjustalex/e-commerce-microservices/assets/21158649/39d6fbef-6d30-4e7c-a270-561ea19f97ce)

#### OrderCreateEvent, OrderStatusUpdateEvent, ProductsQuantityUpdateEvent

OrderCreateEvent event is generated by orders-ms when the user makes the order. The order is initially in the PENDING state (status) and if products-ms consumes the event and approves it (checks availability of products), then OrderStatusUpdateEvent, ProductsQuantityUpdateEvent are sent from products-ms for orders-ms to update its collections.

![image](https://github.com/heyimjustalex/e-commerce-microservices/assets/21158649/a901534b-1027-4e4f-a181-822da0927f8c)
![image](https://github.com/heyimjustalex/e-commerce-microservices/assets/21158649/293f9f76-95a0-4ada-8f81-47e1e9882bf5)

![image](https://github.com/heyimjustalex/e-commerce-microservices/assets/21158649/d6a8f0a5-89bc-4216-93d4-ca39bc2b03df)
![image](https://github.com/heyimjustalex/e-commerce-microservices/assets/21158649/caba81d4-1709-4c4c-b3c7-b042f17c3e36)

## Broker

For the message broker a containerized version of Kafka is used with zookeeper software providing broker’s configuration. To communicate between Kafka and backend services aiokafka package is used by backend. Kafka broker is a single point of failure for the microservices that use it for event emitting (orders-ms, products-ms). There is only a single instance of Kafka broker in the infrastructure.

## Frontend

Frontend is executed in the client's browser (client-side rendering) and was developed with React.js + Vite + VanillaJS + Bootstrap. The code uses a custom hook for http request and global contexts (AuthContext, CartContext) for JWT and cart management. Token is stored in LocalStorage and the design is responsive. Production version of frontend is deployed with 2-stage build and is hosted with nginx server. Production build is generated with ‘vite build’ command underneath. 


## Reverse-proxy / Ingress

Reverse proxy is used to distribute requests between frontend and API. For development there is an nginx used with conf file. For production there is an ingress configuration also based on nginx with in-line certificates (base64 encoded) and in-line config file.

## Deployment
For deployment I use GCP (GKE) with IAC configuration files. The infrastructure creation is not fully automated due to DNS configuration and dynamic LoadBalancer public IP, but steps for configuration are listed in README.md.

### IAC
For IAC I use Terraform with hashicorp/google 4.0 provider. The configuration allows nodes to be scaled up dynamically. The nodes are e2-medium instances.

### CI/CD

For CI/CD CircleCI is used that is connected to Github. After every commit to the main branch workflows are triggered and new Docker images are deployed to Dockerhub. Then the images are downloaded by GCP K8S to the infrastructure and pods are recreated. Relevant secrets for GCP are stored in the CircleCI platform and used by scripts to authenticate and modify the GCP cluster.

![image](https://github.com/heyimjustalex/e-commerce-microservices/assets/21158649/e1d5e9fc-0bb0-4a70-b341-e1cc664d0eb9)


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

