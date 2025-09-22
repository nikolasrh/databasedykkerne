using Dapper;

using Microsoft.Data.SqlClient;

using Npgsql;

using Oracle.ManagedDataAccess.Client;

namespace DapperApp.Tests;

public class DatabaseConnectionTests
{
    [Fact(Timeout = 1000, Skip = "Database disabled")]
    public async Task TestSqlServerConnection()
    {
        var connectionString = "Server=localhost,1433;Database=dapper_fluentmigrator_db;User Id=dapper_user;Password=Password123!;TrustServerCertificate=true;";

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

    [Fact(Timeout = 1000, Skip = "Database disabled")]
    public async Task TestPostgreSqlConnection()
    {
        var connectionString = "Host=localhost;Port=5432;Database=dapper_fluentmigrator_db;Username=dapper_user;Password=Password123!;";

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

    [Fact(Timeout = 1000, Skip = "Database disabled")]
    public async Task TestOracleConnection()
    {
        var connectionString = "Data Source=localhost:1521/FREEPDB1;User Id=dapper_user;Password=Password123!;";

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
