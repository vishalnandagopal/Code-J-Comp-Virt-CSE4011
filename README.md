# Virtualisation CSE4011 J-Component - VIT Chennai

Flask (Python) project submitted for Virtualisation J-Component.

# Project details

# Technical details

Backend only, meant to be run as a docker container. It is written in Python and the web server is built using Flask.

# Running the app

> Docker is the best way to run the app, since it removes issues with dependencies not working on your specific OS. This project has been tested on the `python:3.12-slim` image.

1. Install docker

    Install docker engine from [here](https://docs.docker.com/engine/install/).

    After installation, verify by running `docker --version` in your terminal.

2. Clone the repo

    ```bash
    git clone https://github.com/vishalnandagopal/Code-J-Comp-Virt-CSE4011
    ```

3. Change directory

    ```bash
    cd Code-J-Comp-Virt-CSE4011
    ```

4. Build the image. Make sure this command is being run in the directory where the Dockerfile exists.

    ```bash
    docker build .
    ```

    A SHA256 output (hash of the docker image) will be given at the end of the build command. Copy it for the next step.

5. Run the image

    You can run the project in 2 ways after building the image

    1. Use docker run

        ```bash
        docker run -p 8000:8000 sha256:hash
        ```

        This exposes the 8000 port inside the container/VM (where the flask app is running in your actual computer). Without the -p flag, you cannot access it from your normal browser or some external script.

    2. Use docker-compose

        You can also use docker compose (if you are familiar with it) to directly build it and have it running with the relevant ports and environments set. You have to run this command in the same command as the [docker-compose.yaml](./docker-compose.yaml) file. Verify docker-compose is installed by running `docker-compose --version` in your terminal before running it.

        ```bash
        docker-compose up
        ```
