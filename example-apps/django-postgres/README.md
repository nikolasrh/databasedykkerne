# Django REST API with PostgreSQL

A Django REST API boilerplate with a PostgreSQL database, configured for use with VS Code Dev Containers.

## Prerequisites

- Docker
- VS Code + Dev Containers extension

## Getting Started

1.  Open the `django-postgres` folder in VS Code.
2.  Run the `Dev Containers: Reopen in Container` command.
3.  Wait for the container to build and start.
4.  Run the initial database migrations:
    ```bash
    python backend/manage.py migrate
    ```

## Usage

Once the container is running, you can manage the application from the VS Code terminal.

-   **Run the development server:**
    ```bash
    python backend/manage.py runserver 0.0.0.0:8000
    ```
    The API will be available at `http://localhost:8000/api/`.

-   **Database Migrations:**
    ```bash
    python backend/manage.py makemigrations
    python backend/manage.py migrate
    ```

## Local Development (without Dev Container)

If you prefer not to use Dev Containers, you can run the application using `docker-compose`:

1.  **Build the Docker image:**
    ```bash
    docker-compose build
    ```

2.  **Run the initial migrations:**
    You can run the migrations in two ways:

    *   Directly with `docker-compose`:
        ```bash
        docker-compose run --rm web python backend/manage.py migrate
        ```

    *   Using the provided helper script:
        ```bash
        ./manage.sh migrate
        ```

3.  **Start the services:**
    ```bash
    docker-compose up
    ```

## Setup Explained

This dev container setup is defined by three main files:

-   **`.devcontainer/devcontainer.json`**: This file tells VS Code how to configure the dev container. It specifies the Docker Compose file to use, the service to run, the workspace folder, and other settings.
-   **`docker-compose.yml`**: This file defines the services that make up the development environment. It includes the `web` service for the Django application and the `db` service for the PostgreSQL database.
-   **`Dockerfile`**: This file defines the Docker image for the `web` service. It starts from a Microsoft-provided Python image, creates a virtual environment, and installs the project dependencies from `requirements.txt`.