import os

import yaml
from testing.testing import Testing
import time
import requests
import subprocess
import textwrap

class SidecarInjection(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Sidecar Injection"
        self.mitre_tactic = "TA0002"
        self.mitre_technique = "T1610"
        self.microsoft_technique = "MS-TA9011"
        self.pod = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: simple-application
  labels:
    app: simple-application
spec:
  replicas: 1
  selector:
    matchLabels:
      app: simple-application
  template:
    metadata:
      labels:
        app: simple-application
    spec:
      containers:
      - name: application
        image: simple-application-image
        imagePullPolicy: Always
        ports:
        - containerPort: 80
"""
    def run_attack(self):
        if self.check_install_kubectl() and self.check_install_docker():
            # Deploying simple web server
            print("# Deploying simple web server...")
            self.deploy_simple_web_server()

            # Ensure Deployment is ready
            #print("# Waiting for Deployment to be ready...")
            #while not self.kubectl_is_deployment_ready("simple-application"):
                #time.sleep(1)

            # Modifying Deployment to add evil-sidecar-proxy
            print("# Modifying Deployment to add evil-sidecar-proxy...")
            self.modify_deployment_and_deploy_evil_sidecar_proxy()
            #time.sleep(1)

            # Verification
            print("\n# Verifying Deployment changes...")
            self.kubectl_describe("deployment", "simple-application")

            # Verify web server modification
            print("\n# Verifying web server modification...")
            self.verify_web_server_modification()

            # Cleanup
            # self.cleanup()
      
    def deploy_simple_web_server(self):
        # Write the Go code for the simple web server
        go_code = """package main

import (
    "fmt"
    "log"
    "net/http"
)

func rootHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "text/html")
    w.WriteHeader(http.StatusOK)
    fmt.Fprintln(w, "Hello World!")
}

func main() {
    http.HandleFunc("/", rootHandler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
"""

        # Write the Go code to a file
        with open("main.go", "w") as file:
            file.write(go_code)

        # Write the Dockerfile for the simple web server
        dockerfile = """FROM golang:alpine as builder
RUN mkdir /build 
ADD . /build/
WORKDIR /build 
RUN GO111MODULE=off CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-extldflags "-static"' -o main .
FROM scratch
COPY --from=builder /build/main /app/
WORKDIR /app
CMD ["./main"]
"""

        # Write the Dockerfile to a file
        with open("Dockerfile", "w") as file:
            file.write(dockerfile)

        # Build the simple web server container
        os.system("sudo docker build -t simple-application-image .")

        # Write the YAML text to a file
        with open("simple-webserver.yaml", "w") as file:
            file.write(textwrap.dedent(self.pod))

        self.kubectl_apply("simple-webserver.yaml")


    def modify_deployment_and_deploy_evil_sidecar_proxy(self):
        try:
            # Create Nginx configuration for the evil-sidecar-proxy
            nginx_conf = """error_log /dev/stdout info;
events {
worker_connections  4096;
}

http {
include    mime.types;
access_log /dev/stdout;

    server {
            listen 80 ;
            listen [::]:80 ;

            server_name _;

            location / {
                proxy_pass http://localhost:8080;
                sub_filter 'Hello World!'  'Hello Evil World!';
            }
    }
}
"""

            # Write the Nginx configuration to a file
            with open("nginx.conf", "w") as file:
                file.write(nginx_conf)

            # Write the Dockerfile for the evil-sidecar-proxy
            dockerfile = """FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
"""

            # Write the Dockerfile to a file
            with open("evil-sidecar-proxy-Dockerfile", "w") as file:
                file.write(dockerfile)

            # Build the evil-sidecar-proxy container
            os.system("sudo docker build -t evil-sidecar-proxy -f evil-sidecar-proxy-Dockerfile .")

            # Patch the existing Deployment to add the evil-sidecar-proxy container
            subprocess.run(["kubectl", "patch", "deployment", "simple-application", "-p", '{"spec":{"template":{"spec":{"containers":[{"name":"evil-sidecar-proxy","image":"evil-sidecar-proxy","imagePullPolicy":"Always","ports":[{"containerPort":80}]}]}}}}'])
            print("Evil sidecar proxy added to the deployment.")
            
        except Exception as e:
            print(f"Error: {e}")


    def verify_web_server_modification(self):
        # Send a request to the web server and check the response
        response = self.send_http_request("http://localhost:8080")
        if response == "Hello Evil World!":
            print("Web server successfully modified by evil-sidecar-proxy.")
        else:
            print("Web server modification failed.")

    def cleanup(self):
        # Delete simple web server deployment
        print("# Deleting simple web server deployment...")
        self.kubectl_delete("deployment", "simple-application")

        # Delete evil-sidecar-proxy deployment
        print("# Deleting evil-sidecar-proxy deployment...")
        self.kubectl_delete("deployment", "evil-sidecar-proxy")

        # Delete files
        print("# Deleting all created Files...")
        os.system("rm main.go Dockerfile simple-application.yaml nginx.conf evil-sidecar-proxy-Dockerfile")
        
        if self.docker:
            print("# Unistall Docker")
            self.uninstall_docker()

        if self.kubectl:
            print("# Unistall Kubectl")
            self.uninstall_kubectl()


    def send_http_request(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to send HTTP request. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred while sending HTTP request: {str(e)}")
            return None

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass