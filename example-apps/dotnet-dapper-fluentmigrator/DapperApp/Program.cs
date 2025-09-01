using Dapper;

using DapperApp;

using Microsoft.Data.SqlClient;


using var connection = new SqlConnection("Server=host.docker.internal,1433;Database=msdb;User Id=sa;Password=Password123!;TrustServerCertificate=true;");

var users = connection.Query<User>("SELECT Id, Name FROM Users");

Console.WriteLine($"Found {users.Count()} users in the database.");
