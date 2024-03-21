# Define the Docker command
$dockerCommand = "docker cp auth-microservice:/app/test_results.xml ."

# Execute the Docker command
Invoke-Expression -Command $dockerCommand
