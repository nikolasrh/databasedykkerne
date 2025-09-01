using Dapper;

using Microsoft.Data.SqlClient;

using Npgsql;

using Oracle.ManagedDataAccess.Client;

namespace DapperApp.Tests;

public class DatabaseConnectionTests
{
    [Fact(Timeout = 1000)]
    public async Task TestSqlServerConnection()
    {
        var connectionString = "Server=host.docker.internal,1433;Database=msdb;User Id=sa;Password=Password123!;TrustServerCertificate=true;";

        using var connection = new SqlConnection(connectionString);

        try
        {
            await connection.OpenAsync();
            var result = await connection.QuerySingleAsync<int>("SELECT 1");
            Assert.Equal(1, result);
        }
        catch (Exception ex)
        {
            Assert.Fail($"Should be able to connect to SQL Server database: {ex.Message}");
        }
    }

    [Fact(Timeout = 1000)]
    public async Task TestPostgreSqlConnection()
    {
        var connectionString = "Host=host.docker.internal;Port=5432;Database=postgres;Username=postgres;Password=password;";

        using var connection = new NpgsqlConnection(connectionString);

        try
        {
            await connection.OpenAsync();
            var result = await connection.QuerySingleAsync<int>("SELECT 1");
            Assert.Equal(1, result);
        }
        catch (Exception ex)
        {
            Assert.Fail($"Should be able to connect to PostgreSQL database: {ex.Message}");
        }
    }

    [Fact(Timeout = 1000)]
    public async Task TestOracleConnection()
    {
        var connectionString = "Data Source=host.docker.internal:1521/FREEPDB1;User Id=system;Password=password;";

        using var connection = new OracleConnection(connectionString);

        try
        {
            await connection.OpenAsync();
            var result = await connection.QuerySingleAsync<int>("SELECT 1 FROM DUAL");
            Assert.Equal(1, result);
        }
        catch (Exception ex)
        {
            Assert.Fail($"Should be able to connect to Oracle database: {ex.Message}");
        }
    }
}
