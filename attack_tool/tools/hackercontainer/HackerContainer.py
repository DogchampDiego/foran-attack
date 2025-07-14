#!/usr/bin/python3
import subprocess

class HackerContainer():
    
    def __init__(self):
        download_docker()
        launch_hacker_container()


def download_docker():
    try:
        # Check if Docker is already installed
        subprocess.check_output(["docker", "--version"], stderr=subprocess.STDOUT, text=True)
        print("Docker is already installed on this system.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print("Docker is not installed on this system.")
        try:
            # Download Docker
            subprocess.run(["curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"], check=True)
            subprocess.run(["sudo", "sh", "get-docker.sh"], check=True)
            subprocess.run(["rm", "get-docker.sh"], check=True)
            print("Docker has been installed.")
        except subprocess.CalledProcessError:
            print("Failed to download and install Docker.")

def launch_hacker_container():
    try:
        # Launch the Hacker Container
        print("Launching the Hacker Container...")
        subprocess.run(["sudo", "docker", "run", "--rm", "-it", "--name", "hacker-container", "madhuakula/hacker-container"], check=True)        
    except subprocess.CalledProcessError:
        print("Failed to launch the Docker container.")

