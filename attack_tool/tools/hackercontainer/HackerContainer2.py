#!/usr/bin/python3
import docker

# Initialize the Docker client
client = docker.from_env()

# Define the Docker image and container name
image_name = "madhuakula/hacker-container"
container_name = "hacker_container"

client.containers.run("ubuntu:latest", "echo hello world")


def other():
    # Create a Docker container
    container = client.containers.create(image=image_name, name=container_name)

    # Start the Docker container
    container.start()

    # Check if the container is running
    if container.status == "running":
        print(f"Container {container_name} is running.")

    # Stop the Docker container
    container.stop()

    # Remove the Docker container
    container.remove()

    print(f"Container {container_name} has been removed.")
