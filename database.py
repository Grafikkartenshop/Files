import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection = None
        self.cursor = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print(f"Verbunden mit Datenbank: {database}")
        except Error as e:
            print(f"Datenbankfehler: {e}")

    def get_alle_artikel_daten(self):
        try:
            # Wir nutzen hier dictionary=False nur für die Tabellen-Anzeige (Treeview)
            temp_cursor = self.connection.cursor(dictionary=False)
            query = "SELECT id, name, ek_preis, vk_preis, bestand FROM gpus"
            temp_cursor.execute(query)
            result = temp_cursor.fetchall()
            temp_cursor.close()
            return result
        except Error as e:
            print(f"Fehler beim Laden: {e}")
            return []

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

    def artikel_loeschen(self, id):
        query = "DELETE FROM gpus WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()