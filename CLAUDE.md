# Structure
- ./docker-compose.yml: Contains databases and MCP server
- ./docker: Init scripts for each Docker Compose service
- ./example-apps: Apps used to showcase different libraries and frameworks for working with databases
- ./example-apps/<app-name>/.devcontainer/devcontainer.json: Configures a Dev Container and VS Code extensions and settings

# Workflow
- Run one database at a time along with its MCP server
- MCP servers are defined in .vscode/mcp.json
- Each database has init scripts that create users/databases for each example app
- There are no overlap between example apps when it comes to databases/schemas/users
- Only work at one example app at a time
- Keep each app simple and to the point
- Apps are meant to be developed in VS Code with Dev Containers, and devcontainer.json includes extensions needed for linting, debugging etc.
- Run tests in Dev Containers with docker exec, and use the container name set in devcontainer.json
- Each app should:
    - Be a console app or light weight web app
    - Define needed VS Code extensions 
    - Have a test framework that checks for valid database connections
    - Have a README.md in Norwegian with a description and useful commands for starting the app and running tests
- When creating applcations, try to use CLI tools and document the commands used in the README.md for that app
