from database import DatabaseManager

class GPUHandel:
    def __init__(self, db_manager):
        self.db = db_manager

    def neuen_artikel_registrieren(self, id, name, ek, vk, mindest):
        self.db.artikel_anlegen(id, name, ek, vk, mindest)
        print(f"Artikel {name} erfolgreich angelegt.")

    def wareneingang(self, id, menge):
        artikel = self.db.get_artikel(id)
        if artikel:
            neuer_bestand = artikel['bestand'] + menge
            self.db.update_bestand(id, neuer_bestand)
            print(f"Wareneingang gebucht. Neuer Bestand von {artikel['name']}: {neuer_bestand}")
        else:
            print("Artikel nicht gefunden!")

    def verkauf_abwickeln(self, id, menge):
        artikel = self.db.get_artikel(id)
        if not artikel:
            print("Fehler: Artikel existiert nicht.")
            return

        if artikel['bestand'] < menge:
            print(f"Abbruch: Nicht genügend Lagerbestand! (Vorhanden: {artikel['bestand']})")
            return

        # Logik-Berechnung
        neuer_bestand = artikel['bestand'] - menge
        umsatz = menge * artikel['vk_preis']
        gewinn = menge * (artikel['vk_preis'] - artikel['ek_preis'])

        # Datenbank Update
        self.db.update_bestand(id, neuer_bestand)

        # Output & Warnung
        print(f"--- Verkauf erfolgreich ---")
        print(f"Umsatz: {umsatz:.2f}€ | Gewinn: {gewinn:.2f}€")

        if neuer_bestand <= artikel['mindestbestand']:
            print(f"WARNUNG: Mindestbestand unterschritten! Rest: {neuer_bestand}")

# Beispielhafter Programmablauf
if __name__ == "__main__":
    # Verbindungsdaten anpassen
    db = DatabaseManager("localhost", "root", "", "gpu_shop")
    handel = GPUHandel(db)

    # 1. Artikel anlegen
    # handel.neuen_artikel_registrieren("RTX4080", "NVIDIA RTX 4080", 850.00, 1199.00, 3)

    # 2. Wareneingang
    handel.wareneingang("RTX4080", 10)

    # 3. Verkauf
    handel.verkauf_abwickeln("RTX4080", 8)