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


    def registriere_verkauf(self, gpu_id, menge, umsatz, gewinn):
        """Speichert einen getätigten Verkauf in der sales-Tabelle."""
        try:
            query = "INSERT INTO sales (gpu_id, menge, umsatz, gewinn) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (gpu_id, menge, umsatz, gewinn))
            self.connection.commit()
        except Error as e:
            print(f"Fehler beim Speichern des Verkaufs: {e}")

    def get_alle_artikel_daten(self):
        try:
            temp_cursor = self.connection.cursor(dictionary=False)
            query = "SELECT id, name, ek_preis, vk_preis, bestand FROM gpus"
            temp_cursor.execute(query)
            result = temp_cursor.fetchall()
            temp_cursor.close()
            return result
        except Error as e:
            print(f"Fehler beim Abrufen der Liste: {e}")
            return []

    def artikel_anlegen(self, id, name, ek, vk, mindest):
        try:
            query = "INSERT INTO gpus (id, name, ek_preis, vk_preis, mindestbestand) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (id, name, ek, vk, mindest))
            self.connection.commit()
            return True
        except Error as e:
            raise Exception(f"Fehler beim Anlegen: {e}")

    def artikel_loeschen(self, id):
        try:
            query = "DELETE FROM gpus WHERE id = %s"
            self.cursor.execute(query, (id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Fehler beim Löschen: {e}")
            return False

    def get_artikel(self, id):
        query = "SELECT * FROM gpus WHERE id = %s"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()

    def update_bestand(self, id, neuer_bestand):
        try:
            query = "UPDATE gpus SET bestand = %s WHERE id = %s"
            self.cursor.execute(query, (neuer_bestand, id))
            self.connection.commit()
        except Error as e:
            print(f"Fehler beim Update: {e}")

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()