using Dapper;

using DapperApp;

using Microsoft.Data.SqlClient;


using var connection = new SqlConnection("Server=host.docker.internal,1433;Database=dapper_fluentmigrator_db;User Id=dapper_user;Password=Password123!;TrustServerCertificate=true;");

var users = connection.Query<User>("SELECT Id, Name FROM Users");

Console.WriteLine($"Found {users.Count()} users in the database.");
