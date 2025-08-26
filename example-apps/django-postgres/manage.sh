#!/bin/bash
# A wrapper script for running manage.py commands within the Docker container.
docker-compose run --rm web python backend/manage.py "$@"
