package com.example

import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.Table
import org.jetbrains.exposed.sql.transactions.transaction

object Pokemon : Table("pokemon") {
    val id = integer("id").autoIncrement()
    val name = varchar("name", 255)
    override val primaryKey = PrimaryKey(id)
}

fun runPokemonMigrations() {
    val url = "jdbc:postgresql://host.docker.internal:5432/postgres"
    val user = "postgres"
    val password = "password"
    try {
        val db =
                Database.connect(
                        url,
                        driver = "org.postgresql.Driver",
                        user = user,
                        password = password
                )
        transaction(db) { SchemaUtils.create(Pokemon) }
        println("Migration complete: 'pokemon' table created (if not exists).")
    } catch (e: Exception) {
        println("Migration failed: ${e.message}")
    }
}
