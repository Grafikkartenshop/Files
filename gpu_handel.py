class GPUHandel:
    def __init__(self, db_manager):
        self.db = db_manager

    def get_alle_artikel(self):
        return self.db.get_alle_artikel_daten()

    def neuen_artikel_registrieren(self, id, name, ek, vk, mindest):
        if not id or not name:
            raise ValueError("ID und Name dürfen nicht leer sein.")
        self.db.artikel_anlegen(id, name, ek, vk, mindest)

    def artikel_loeschen(self, gpu_id):
        return self.db.artikel_loeschen(gpu_id)

    def wareneingang(self, id, menge):
        if menge <= 0:
            raise ValueError("Menge muss positiv sein.")
        artikel = self.db.get_artikel(id)
        if artikel:
            neuer_bestand = artikel['bestand'] + menge
            self.db.update_bestand(id, neuer_bestand)
        else:
            raise Exception("Artikel nicht gefunden.")

    def verkauf_abwickeln(self, id, menge):
        if menge <= 0:
            raise ValueError("Menge muss positiv sein.")
        artikel = self.db.get_artikel(id)
        if not artikel:
            raise Exception("Artikel existiert nicht.")

        if artikel['bestand'] < menge:
            raise Exception(f"Zu wenig Bestand! ({artikel['bestand']} vorhanden)")

        neuer_bestand = artikel['bestand'] - menge
        self.db.update_bestand(id, neuer_bestand)