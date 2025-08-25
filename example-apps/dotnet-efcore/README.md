# Entity Framework Core (EF Core) example app

Commands used to create solution:

```
dotnet new gitignore
dotnet new editorconfig
dotnet new sln -n EFCoreApp
dotnet new console -n EFCoreApp
dotnet new xunit -n EFCoreApp.Tests
dotnet add EFCoreApp.Tests reference EFCoreApp
dotnet sln add EFCoreApp
dotnet sln add EFCoreApp.Tests
```

Add dependencies:

```
dotnet add EFCoreApp package Microsoft.EntityFrameworkCore.SqlServer
```
