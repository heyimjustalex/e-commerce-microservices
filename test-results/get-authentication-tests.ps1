# Define the Docker command
$dockerCommand = "docker cp authentication-ms:/app/test_results.xml ."

# Execute the Docker command
Invoke-Expression -Command $dockerCommand
