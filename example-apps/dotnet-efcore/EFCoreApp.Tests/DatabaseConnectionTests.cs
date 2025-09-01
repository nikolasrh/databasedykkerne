using Microsoft.EntityFrameworkCore;

namespace EFCoreApp.Tests;

public class DatabaseConnectionTests
{
    [Fact(Timeout = 1000)]
    public async Task TestSqlServerConnection()
    {
        var connectionString = "Server=host.docker.internal,1433;Database=msdb;User Id=sa;Password=Password123!;TrustServerCertificate=true;";
        var options = new DbContextOptionsBuilder<PersonContext>()
            .UseSqlServer(connectionString)
            .Options;
        using var context = new PersonContext(options);

        var canConnect = await context.Database.CanConnectAsync();

        Assert.True(canConnect, "Should be able to connect to SQL Server database");
    }

    [Fact(Timeout = 1000)]
    public async Task TestPostgreSqlConnection()
    {
        var connectionString = "Host=host.docker.internal;Port=5432;Database=postgres;Username=postgres;Password=password;";
        var options = new DbContextOptionsBuilder<PersonContext>()
            .UseNpgsql(connectionString)
            .Options;
        using var context = new PersonContext(options);

        var canConnect = await context.Database.CanConnectAsync();

        Assert.True(canConnect, "Should be able to connect to PostgreSQL database");
    }

    [Fact(Timeout = 1000)]
    public async Task TestOracleConnection()
    {
        var connectionString = "Data Source=host.docker.internal:1521/FREEPDB1;User Id=system;Password=password;";
        var options = new DbContextOptionsBuilder<PersonContext>()
            .UseOracle(connectionString)
            .Options;
        using var context = new PersonContext(options);

        var canConnect = await context.Database.CanConnectAsync();

        Assert.True(canConnect, "Should be able to connect to Oracle database");
    }
}
