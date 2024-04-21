# Delete commands
declare -a deleteCommands=(
    # 'kubectl delete -f ./infrastracture/kubernetes/proxy.yaml'
    'kubectl delete -f ./infrastracture/kubernetes/gateway.yaml'
    'kubectl delete -f ./infrastracture/kubernetes/frontend.yaml'
    'kubectl delete -f ./infrastracture/kubernetes/orders.yaml'
    'kubectl delete -f ./infrastracture/kubernetes/authentication.yaml'
    'kubectl delete -f ./infrastracture/kubernetes/products.yaml'
    'kubectl delete -f ./infrastracture/kubernetes/orders-db.yaml'
    'kubectl delete -f ./infrastracture/kubernetes/authentication-db.yaml'
    'kubectl delete -f ./infrastracture/kubernetes/products-db.yaml'
    'kubectl delete -f ./infrastracture/kubernetes/message-broker.yaml'
    'kubectl delete -f ./infrastracture/kubernetes/zookeeper.yaml'
)

# Execute delete commands
for command in "${deleteCommands[@]}"; do
    $command
done

declare -a applyCommands=(
    'kubectl apply -f ./infrastracture/kubernetes/zookeeper.yaml'
    'kubectl apply -f ./infrastracture/kubernetes/orders-db.yaml'
    'kubectl apply -f ./infrastracture/kubernetes/authentication-db.yaml'
    'kubectl apply -f ./infrastracture/kubernetes/products-db.yaml'
    'kubectl apply -f ./infrastracture/kubernetes/message-broker.yaml'
    'kubectl apply -f ./infrastracture/kubernetes/frontend.yaml'
    'kubectl apply -f ./infrastracture/kubernetes/orders.yaml'
    'kubectl apply -f ./infrastracture/kubernetes/authentication.yaml'
    'kubectl apply -f ./infrastracture/kubernetes/products.yaml'
    'kubectl apply -f ./infrastracture/kubernetes/gateway.yaml'
    # 'kubectl apply -f ./infrastracture/kubernetes/proxy.yaml'
)

# Execute apply commands
for command in "${applyCommands[@]}"; do
    $command
done
