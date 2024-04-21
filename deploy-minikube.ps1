$deleteCommands = @(
    'kubectl delete -f .\infrastracture\kubernetes\proxy.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\gateway.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\frontend.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\orders.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\authentication.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\products.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\orders-db.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\authentication-db.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\products-db.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\message-broker.yaml',
    'kubectl delete -f .\infrastracture\kubernetes\zookeeper.yaml'
)

foreach ($command in $deleteCommands) {
    Invoke-Expression -Command $command
}

$applyCommands = @(
    'kubectl apply -f .\infrastracture\kubernetes\zookeeper.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\orders-db.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\authentication-db.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\products-db.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\message-broker.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\frontend.yaml',    
    'kubectl apply -f .\infrastracture\kubernetes\orders.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\authentication.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\products.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\gateway.yaml',
    'kubectl apply -f .\infrastracture\kubernetes\proxy.yaml'
)

foreach ($command in $applyCommands) {
    Invoke-Expression -Command $command
}
