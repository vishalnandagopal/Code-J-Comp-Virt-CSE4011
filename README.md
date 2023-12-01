# Virtualisation CSE4011 J-Component - VIT Chennai

Flask (Python) project submitted for Virtualisation J-Component.

# Project details

# Technical details

Backend only, meant to be run as a docker container. It is written in Python and the web server is built using Flask.

# Running the app

There are 2 ways to run this app.

1. Through Docker
2. Directly running the app

> Docker is the best way to run the app, since it removes issues with dependencies not working on your specific OS. This project has been tested on the `python:3.12-slim` image.

## Docker Method

1. Install docker

    Install the Docker engine from [here](https://docs.docker.com/engine/install/).

    After installation, verify by running `docker --version` in your terminal.

2. Clone the repo

    ```bash
    git clone https://github.com/vishalnandagopal/Code-J-Comp-Virt-CSE4011
    ```

3. Change directory

    ```bash
    cd Code-J-Comp-Virt-CSE4011
    ```

4. Build the image. Make sure this command is being run in the same directory as the Dockerfile exists.

    ```bash
    docker build .
    ```

    A SHA256 output (hash of the docker image) will be given at the end of the build command. Copy it for the next step. (copy the entire `sha256:hash` part)

5. Run the image

    You can run the project in 2 ways after building the image

    1. Use docker run

        ```bash
        docker run -p 8000:8000 sha256:hash
        ```

        This exposes the 8000 port inside the container/VM (where the flask app is running in your actual computer). Without the -p flag, you cannot access it from your normal browser or some external script.

    2. Use docker-compose

        You can also use docker compose to directly build it and have it running with the relevant ports and environments set.

        You have to run this command in the same folder as the [docker-compose.yaml](./docker-compose.yaml) file. Verify docker-compose is installed by running `docker-compose --version` in your terminal before running it.

        ```bash
        docker-compose up
        ```

6. Run the demo script in a separate terminal to show some input/output
    ```bash
    python demo.py
    ```

## Running the app without Docker

1. Clone the repo

    ```bash
    git clone https://github.com/vishalnandagopal/Code-J-Comp-Virt-CSE4011
    ```

2. Change directory

    ```bash
    cd Code-J-Comp-Virt-CSE4011
    ```

3. Create a virtual environment using `venv` (Highly recommended to avoid conflicts between previously installed libraries and their own dependencies)

    ```bash
    python -m venv .venv
    ```

    This creates a virtual environment with no packages at `.venv/`

4. Activate venv

    On Linux and similar systems

    ```bash
    source ./venv/bin/activate
    ```

    On Windows,

    ```cmd
    .venv\Scripts\activate
    ```

5. Install the required libraries

    ```bash
    pip install -r requirements.txt
    ```

6. Run the app

    ```bash
    python app.py
    ```

7. Run the demo script in a separate terminal to show some input/output
    ```bash
    python demo.py
    ```
