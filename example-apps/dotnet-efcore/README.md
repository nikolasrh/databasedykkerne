# Entity Framework Core (EF Core) example app

## Commands

Run application:

```
dotnet run --project EFCoreApp
```

Run application with hot reload:

```
dotnet watch run --project EFCoreApp
```

Run all tests in solution:

```
dotnet test
```

Auto re-run tests:

```
cd EFCoreApp.Tests
dotnet watch test
```

## Commands used to create application

Create solution and projects:

```
dotnet new gitignore
dotnet new editorconfig
dotnet new sln -n EFCoreApp
dotnet new console -n EFCoreApp
dotnet new xunit -n EFCoreApp.Tests
dotnet sln add EFCoreApp
dotnet sln add EFCoreApp.Tests
```

Add dependencies:

```
dotnet add EFCoreApp package Microsoft.EntityFrameworkCore.SqlServer
dotnet add EFCoreApp.Tests reference EFCoreApp
```
