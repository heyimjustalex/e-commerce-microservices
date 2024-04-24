$deleteCommands = @(
    'kubectl delete -f .\infrastructure\kubernetes\minikube\proxy.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\minikube\gateway.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\minikube\frontend.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\minikube\orders.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\minikube\authentication.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\minikube\products.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\minikube\orders-db.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\minikube\authentication-db.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\minikube\products-db.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\minikube\message-broker.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\minikube\zookeeper.yaml'
)

foreach ($command in $deleteCommands) {
    Invoke-Expression -Command $command
}

$applyCommands = @(
    'kubectl apply -f .\infrastructure\kubernetes\minikube\zookeeper.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\minikube\orders-db.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\minikube\authentication-db.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\minikube\products-db.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\minikube\message-broker.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\minikube\frontend.yaml',    
    'kubectl apply -f .\infrastructure\kubernetes\minikube\orders.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\minikube\authentication.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\minikube\products.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\minikube\gateway.yaml'
    'kubectl apply -f .\infrastructure\kubernetes\minikube\proxy.yaml'
)

foreach ($command in $applyCommands) {
    Invoke-Expression -Command $command
}
