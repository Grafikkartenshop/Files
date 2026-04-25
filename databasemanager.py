import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self):
        self.config = {
            'host': "localhost",
            'user': "root",
            'password': "",
            'database': "Grafikkartenshop"
        }

    def get_all_gpus(self):
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Grafikkarte")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Error as e:
            print(f"Fehler beim Abrufen der Grafikkarten: {e}")
            return []

    def get_shop_data(self, shopID):
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Grafikkartenshop WHERE shopID = %s", (shopID,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Error as e:
            print(f"Fehler beim Abrufen der Shop-Daten: {e}")
            return None

    def execute_query(self, query, params=None):
        """
        Universelle Methode für INSERT, UPDATE und DELETE.
        Wird für das Speichern von neuen GPUs, das Löschen und 
        das Aktualisieren von Budget/Umsatz/Bestand genutzt.
        """
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit() # Wichtig, um Änderungen permanent in XAMPP zu speichern
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(f"Fehler beim Ausführen der Abfrage: {e}")
            return False