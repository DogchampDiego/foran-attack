#!/usr/bin/python3
import subprocess
from environment.global_const import GlobalVariables
import docker

# Global variables
global_var = GlobalVariables.get_instance()

# Install MTKPI
path = global_var.get_base_dir() + "tools/mtkpi/install_mtkpi.sh"
print("Installation script path MTKPI: ", path)
subprocess.run(["sudo", "chmod", "+x", path], check=True)
print(f"Script '{path}' is now executable.")
subprocess.call(["bash", path, global_var.get_tool_non_bin_dir(), global_var.get_base_dir()])

# Initialize the Docker client
client = docker.from_env()

# Define the Docker image and container name
image_name = "mtkpi:latest"
container_name = "mtkpi"

# Path to the directory containing the Dockerfile
path_to_dockerfile = global_var.get_tool_non_bin_dir() + "mtkpi"

# Build the image
image, build_log = client.images.build(path=path_to_dockerfile, tag="container_name")

# Output the build logs
for line in build_log:
    if 'stream' in line:
        print(line['stream'].strip())

# Run a container using the built image
container = client.containers.run("container_name", detach=True)

print(f"Running container {container.id} from image ", container_name)

def install():
    path = global_var.get_base_dir() + "tools/badpods/install_badpods.sh"
    print("Installation script path MTKPI: ", path)
    subprocess.run(["sudo", "chmod", "+x", path], check=True)
    print(f"Script '{path}' is now executable.")
    subprocess.call(["bash", path, global_var.get_tool_non_bin_dir(), global_var.get_base_dir()])
    

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
