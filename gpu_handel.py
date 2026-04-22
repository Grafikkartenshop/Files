from database import DatabaseManager

class GPUHandel:
    def __init__(self, db_manager):
        self.db = db_manager

    def get_alle_artikel(self):
        """
        Holt alle Grafikkarten für die Anzeige in der GUI-Tabelle.
        """
        return self.db.get_alle_artikel_daten()

    def get_finanzen(self):
        """
        Holt die globale Finanzstatistik (Gesamtumsatz und Gesamtgewinn).
        Wird von der GUI (refresh_table) aufgerufen.
        """
        return self.db.get_finanz_statistik()

    def neuen_artikel_registrieren(self, id, name, ek, vk, mindest):
        """Registriert ein neues Produkt in der Datenbank."""
        if not id or not name:
            raise ValueError("ID und Name dürfen nicht leer sein.")
        self.db.artikel_anlegen(id, name, ek, vk, mindest)

    def artikel_loeschen(self, gpu_id):
        """Löscht den ausgewählten Artikel komplett aus der Datenbank."""
        if not gpu_id:
            return False
        return self.db.artikel_loeschen(gpu_id)

    def wareneingang(self, id, menge):
        """Erhöht den Bestand einer GPU."""
        if menge <= 0:
            raise ValueError("Menge muss größer als 0 sein.")

        artikel = self.db.get_artikel(id)
        if artikel:
            # Unterstützung für Dictionary (XAMPP/MySQL) oder Tupel
            aktueller_bestand = artikel['bestand'] if isinstance(artikel, dict) else artikel[4]
            neuer_bestand = aktueller_bestand + menge
            self.db.update_bestand(id, neuer_bestand)
        else:
            raise Exception(f"Artikel mit ID {id} nicht gefunden!")

    def verkauf_abwickeln(self, id, menge):
        """Wickelt einen Verkauf ab, aktualisiert den Bestand und speichert die Finanzen."""
        if menge <= 0:
            raise ValueError("Verkaufsmenge muss positiv sein.")

        artikel = self.db.get_artikel(id)
        if not artikel:
            raise Exception(f"Artikel {id} existiert nicht.")

        # Daten-Mapping (Sicherstellung, dass es mit Dictionary-Cursor klappt)
        if isinstance(artikel, dict):
            bestand = artikel['bestand']
            vk_preis = float(artikel['vk_preis'])
            ek_preis = float(artikel['ek_preis'])
            min_bestand = artikel['mindestbestand']
        else:
            # Fallback für Standard-Cursor (Tupel)
            bestand = artikel[4]
            vk_preis = float(artikel[3])
            ek_preis = float(artikel[2])
            min_bestand = artikel[5]

        if bestand < menge:
            raise Exception(f"Lager zu leer! Vorhanden: {bestand}")

        # 1. Bestand in Datenbank aktualisieren
        neuer_bestand = bestand - menge
        self.db.update_bestand(id, neuer_bestand)

        # 2. Finanzwerte berechnen
        umsatz = menge * vk_preis
        gewinn = menge * (vk_preis - ek_preis)

        # 3. NEU: Verkauf permanent in der Datenbank-Tabelle 'sales' registrieren
        # Dies ist nötig, damit die GUI oben die Statistik anzeigen kann!
        self.db.registriere_verkauf(id, menge, umsatz, gewinn)

        # Feedback in Konsole
        print(f"Verkauf: {id} | Umsatz: {umsatz:.2f}€ | Gewinn: {gewinn:.2f}€")

        if neuer_bestand <= min_bestand:
            print(f"WARNUNG: Mindestbestand für {id} unterschritten!")