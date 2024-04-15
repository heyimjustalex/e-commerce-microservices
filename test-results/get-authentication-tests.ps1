# Define the Docker command
$dockerCommand1 = "docker cp authentication-ms:/app/test.xml ./authentication.xml"
$dockerCommand2 = "docker cp products-ms:/app/test.xml ./products.xml"
$dockerCommand3 = "docker cp orders-ms:/app/test.xml ./orders.xml"

# Execute the Docker command
Invoke-Expression -Command $dockerCommand1
Invoke-Expression -Command $dockerCommand2
Invoke-Expression -Command $dockerCommand3
