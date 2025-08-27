# Node.js, Express, and Prisma Starter

This is a simple starter project for building a Node.js application with Express and Prisma. It is configured to run in a Dev Container, which makes it easy to get started.

## Getting Started

1.  Open this project in VS Code.
2.  When prompted, click "Reopen in Container".
3.  The Dev Container will build and start. The `postStartCommand` will run `npm install`, `npx prisma generate`, and start the dev server.

## Database

To connect to a database, you will need to:

1.  Update the `provider` and `url` in the `datasource` block in `prisma/schema.prisma`.
2.  Set the `DATABASE_URL` environment variable.

## Prisma Schema

The `prisma/schema.prisma` file contains a placeholder `Example` model.

## Database Migrations

This project uses Prisma to manage database migrations.

### Development

1.  Edit the `prisma/schema.prisma` file to define your data models.
2.  Run the following command to create and apply a new migration:

    ```bash
    npx prisma migrate dev --name <migration-name>
    ```

### Production

When you deploy your application to production, you will need to run the following command to apply all pending migrations:

```bash
npx prisma migrate deploy
```