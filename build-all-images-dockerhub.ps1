# Define the Docker command
$buildCommand1 = "docker build -t heyimjustalex/authentication-ms -f ./backend/authentication-ms/Dockerfile.prod ./backend/authentication-ms/"
$buildCommand2 = "docker build -t heyimjustalex/orders-ms -f ./backend/orders-ms/Dockerfile.prod ./backend/orders-ms/"
$buildCommand3 = "docker build -t heyimjustalex/products-ms -f ./backend/orders-ms/Dockerfile.prod ./backend/products-ms/"
$buildCommand4 = "docker build -t heyimjustalex/gateway-ms ./backend/gateway-ms/"

$buildCommand5 = "docker build -t heyimjustalex/authentication-db ./db/authentication-db/"
$buildCommand6 = "docker build -t heyimjustalex/orders-db ./db/orders-db/"
$buildCommand7 = "docker build -t heyimjustalex/products-db ./db/products-db/"

#add here your api address for prod build
$buildCommand8 = 'docker build --build-arg="VITE_APP_BACKEND_ADDRESS=https://cloudcomputingtechnologies.pl/api" -t heyimjustalex/frontend -f ./frontend/app/Dockerfile.prod ./frontend/app'
$buildCommand9 = "docker build -t heyimjustalex/nginx-proxy:minikube ./nginx-proxy/prod-minikube"
$buildCommand10 = "docker build -t heyimjustalex/nginx-proxy:docker ./nginx-proxy/prod-docker"
$buildCommand11 = "docker build -t heyimjustalex/frontend:dev -f ./frontend/app/Dockerfile ./frontend/app"
$buildCommand12 = 'docker build --build-arg="VITE_APP_BACKEND_ADDRESS=https://localhost/api" -t heyimjustalex/frontend:minikube -f ./frontend/app/Dockerfile.prod ./frontend/app'

$pushCommand1 = "docker push heyimjustalex/authentication-ms"
$pushCommand2 = "docker push heyimjustalex/orders-ms"
$pushCommand3 = "docker push heyimjustalex/products-ms"
$pushCommand4 = "docker push heyimjustalex/gateway-ms"

$pushCommand5 = "docker push heyimjustalex/authentication-db"
$pushCommand6 = "docker push heyimjustalex/orders-db"
$pushCommand7 = "docker push heyimjustalex/products-db"

$pushCommand8 = "docker push heyimjustalex/frontend"
$pushCommand9 = "docker push heyimjustalex/nginx-proxy:minikube"
$pushCommand10 = "docker push heyimjustalex/nginx-proxy:docker"
$pushCommand11 = "docker push heyimjustalex/frontend:dev"
$pushCommand12 = "docker push heyimjustalex/frontend:minikube"

# Execute the Docker command
Invoke-Expression -Command $buildCommand1
Invoke-Expression -Command $pushCommand1
Invoke-Expression -Command $buildCommand2
Invoke-Expression -Command $pushCommand2
Invoke-Expression -Command $buildCommand3
Invoke-Expression -Command $pushCommand3
Invoke-Expression -Command $buildCommand4
Invoke-Expression -Command $pushCommand4
Invoke-Expression -Command $buildCommand5
Invoke-Expression -Command $pushCommand5
Invoke-Expression -Command $buildCommand6
Invoke-Expression -Command $pushCommand6
Invoke-Expression -Command $buildCommand7
Invoke-Expression -Command $pushCommand7
Invoke-Expression -Command $buildCommand8
Invoke-Expression -Command $pushCommand8
Invoke-Expression -Command $buildCommand9
Invoke-Expression -Command $pushCommand9
Invoke-Expression -Command $buildCommand10
Invoke-Expression -Command $pushCommand10
Invoke-Expression -Command $buildCommand11
Invoke-Expression -Command $pushCommand11
Invoke-Expression -Command $buildCommand12
Invoke-Expression -Command $pushCommand12
 