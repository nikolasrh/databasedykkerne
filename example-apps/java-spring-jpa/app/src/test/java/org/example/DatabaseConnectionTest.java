package org.example;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit.jupiter.EnabledIf;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@EnabledIf(value = "#{environment.matchesProfiles('oracle')}", loadContext = true)
class OracleConnectionTest {

    @Autowired
    private DataSource dataSource;

    @Test
    void testConnection() throws SQLException {

        assertNotNull(dataSource, "DataSource should not be null");

        try (Connection connection = dataSource.getConnection();
                Statement statement = connection.createStatement();
                ResultSet resultSet = statement.executeQuery("SELECT 1 FROM DUAL")) {

            assertTrue(resultSet.next(), "Query should return at least one row");
            assertEquals(1, resultSet.getInt(1), "Query should return 1");
        }
    }
}

@SpringBootTest
@EnabledIf(value = "#{environment.matchesProfiles('postgres')}", loadContext = true)
class PostgreSQLConnectionTest {

    @Autowired
    private DataSource dataSource;

    @Test
    void testConnection() throws SQLException {
        assertNotNull(dataSource, "DataSource should not be null");

        try (Connection connection = dataSource.getConnection();
                Statement statement = connection.createStatement();
                ResultSet resultSet = statement.executeQuery("SELECT 1")) {

            assertTrue(resultSet.next(), "Query should return at least one row");
            assertEquals(1, resultSet.getInt(1), "Query should return 1");
        }
    }
}

@SpringBootTest
@EnabledIf(value = "#{environment.matchesProfiles('mssql')}", loadContext = true)
class SQLServerConnectionTest {

    @Autowired
    private DataSource dataSource;

    @Test
    void testConnection() throws SQLException {
        assertNotNull(dataSource, "DataSource should not be null");

        try (Connection connection = dataSource.getConnection();
                Statement statement = connection.createStatement();
                ResultSet resultSet = statement.executeQuery("SELECT 1")) {

            assertTrue(resultSet.next(), "Query should return at least one row");
            assertEquals(1, resultSet.getInt(1), "Query should return 1");
        }
    }
}
