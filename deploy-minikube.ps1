$deleteCommands = @(
    'kubectl delete -f .\infrastracture\kubernetes\minikube\proxy.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\minikube\gateway.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\minikube\frontend.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\minikube\orders.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\minikube\authentication.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\minikube\products.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\minikube\orders-db.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\minikube\authentication-db.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\minikube\products-db.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\minikube\message-broker.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\minikube\zookeeper.yaml'
)

foreach ($command in $deleteCommands) {
    Invoke-Expression -Command $command
}

$applyCommands = @(
    'kubectl apply -f .\infrastracture\kubernetes\minikube\zookeeper.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\minikube\orders-db.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\minikube\authentication-db.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\minikube\products-db.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\minikube\message-broker.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\minikube\frontend.yaml',    
    'kubectl apply -f .\infrastracture\kubernetes\minikube\orders.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\minikube\authentication.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\minikube\products.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\minikube\gateway.yaml'
    'kubectl apply -f .\infrastracture\kubernetes\minikube\proxy.yaml'
)

foreach ($command in $applyCommands) {
    Invoke-Expression -Command $command
}
