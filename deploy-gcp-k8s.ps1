$deleteCommands = @(
    'kubectl delete -f .\infrastructure\kubernetes\gcp\ingress.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\gcp\gateway.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\gcp\frontend.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\gcp\orders.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\gcp\authentication.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\gcp\products.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\gcp\orders-db.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\gcp\authentication-db.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\gcp\products-db.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\gcp\message-broker.yaml',
    'kubectl delete -f .\infrastructure\kubernetes\gcp\zookeeper.yaml'
)

foreach ($command in $deleteCommands) {
    Invoke-Expression -Command $command
}

$applyCommands = @(
    'kubectl apply -f .\infrastructure\kubernetes\gcp\zookeeper.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\gcp\orders-db.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\gcp\authentication-db.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\gcp\products-db.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\gcp\message-broker.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\gcp\frontend.yaml',    
    'kubectl apply -f .\infrastructure\kubernetes\gcp\orders.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\gcp\authentication.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\gcp\products.yaml',
    'kubectl apply -f .\infrastructure\kubernetes\gcp\gateway.yaml'
    'kubectl apply -f .\infrastructure\kubernetes\gcp\ingress.yaml'
)

foreach ($command in $applyCommands) {
    Invoke-Expression -Command $command
}
