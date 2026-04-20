import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor(dictionary=True)
            self._create_table()
        except Error as e:
            print(f"Fehler bei der Verbindung: {e}")

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS gpus (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100),
            ek_preis DECIMAL(10, 2),
            vk_preis DECIMAL(10, 2),
            bestand INT DEFAULT 0,
            mindestbestand INT DEFAULT 5
        )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def artikel_anlegen(self, id, name, ek, vk, mindest):
        query = "INSERT INTO gpus (id, name, ek_preis, vk_preis, mindestbestand) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (id, name, ek, vk, mindest))
        self.connection.commit()

    def get_artikel(self, id):
        query = "SELECT * FROM gpus WHERE id = %s"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()

    def update_bestand(self, id, neuer_bestand):
        query = "UPDATE gpus SET bestand = %s WHERE id = %s"
        self.cursor.execute(query, (neuer_bestand, id))
        self.connection.commit()

    def close(self):
        self.connection.close()