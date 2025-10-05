Only read files that don't match the .gitignore file.

Don't add reduntant comments to the code when the variable name already describes what it is.

This folder is for a database optimization workshop.

- ./src: Python source code and tests
- ./migrations: Migrations for golang-migrate
- ../docker-compose.yml: PostgreSQL setup in the parent folder

The docker compose file contains multiple services, but this workshop only uses postgres.
The Python environment is not installed on the local machine.
Instead use devcontaienrs to run tests.
Database migrations are run with the golang-migrate container image from the host machine.
When seeding the database, postgres should be running normally.
When running performance tests, postgres should be running with limited resources.

Run initial setup and seed database inside dev container:
````
docker exec -u vscode -w /workspaces/databasedykkerne/performance-app performance-app ./setup.sh --sample
```

Only run without the `--sample` argument if I excplicitly tell you to.

Run tests inside dev container:
```
docker exec -u vscode -w /workspaces/databasedykkerne/performance-app performance-app pytest
```

Run database seeding inside dev container:
```
docker exec -u vscode -w /workspaces/databasedykkerne/performance-app performance-app python src/seed_database.py
```

Start postgres database:
```
docker compose -f ../docker-compose.yml up postgres -d
```

Start postgres database with limited resources:
```
docker compose -f ../docker-compose.yml -f ../docker-compose.resources.yml up postgres -d
```

Database migrations don't need to be executed inside the dev container.
Run the migrate.sh script with the arguments "up" or "down", and the number of migrations to apply.
```
./performance-app/migrate.sh up 1
```
