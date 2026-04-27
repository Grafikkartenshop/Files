import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from databasemanager import DatabaseManager
from grafikkarte import Grafikkarte
from PIL import Image, ImageTk


class Grafikkartenshop:

    def __init__(self, shopID):
        self.__shopID = shopID
        self.__name = None
        self.__umsatz = None
        self.__budget = None
        self.__alleGrafikkarten = []

        db = DatabaseManager()

        shop_daten = db.get_shop_data(self.__shopID)
        if shop_daten:
            self.__name = shop_daten['name']
            self.__umsatz = shop_daten['umsatz']
            self.__budget = shop_daten['budget']
            self.__shopID = shop_daten['shopID']

        self.daten_laden()

    def daten_laden(self):
        db = DatabaseManager()
        rohdaten = db.get_all_gpus()
        self.__alleGrafikkarten = []
        for d in rohdaten:
            gpu = Grafikkarte(d['modell'], d['hersteller'], d['marke'], d['vramGroesse'], d['speichertyp'], d['einkaufspreis'], d['verkaufspreis'])
            gpu.setArtikelNr(d['artikelNr'])
            gpu.setBestand(d['bestand'])
            self.__alleGrafikkarten.append(gpu)

    def getShopID(self):
        return self.__shopID
    
    def getName(self):
        return self.__name
    
    def getUmsatz(self):
        return self.__umsatz
    
    def getBudget(self):
        return self.__budget
    
    def setShopID(self, shopID):
        self.__shopID = shopID

    def setName(self, name):
        self.__name = name

    def setUmsatz(self, umsatz):
        self.__umsatz = umsatz

    def setBudget(self, budget):
        self.__budget = budget

    def shop_finanzen_speichern(self):
        db = DatabaseManager()
        query = "UPDATE Grafikkartenshop SET budget = %s, umsatz = %s WHERE shopID = %s"
        db.execute_query(query, (self.getBudget(), self.getUmsatz(), self.getShopID()))

    def grafikkarteEinkaufen(self, artikelNr, menge) -> bool:
        gpu = self.sucheGrafikkarte(artikelNr)
        if not gpu:
            return False
        gesamtkosten = gpu.getEinkaufspreis() * menge

        if self.getBudget() >= gesamtkosten:
            neuer_bestand = gpu.getBestand() + menge
            
            db = DatabaseManager()
            db.execute_query("UPDATE Grafikkarte SET bestand = %s WHERE artikelNr = %s", (neuer_bestand, artikelNr))
            self.setBudget(self.getBudget() - gesamtkosten)
            self.shop_finanzen_speichern()
            self.daten_laden()
            return True
        else:
            return False

    def grafikkarteVerkaufen(self, artikelNr, menge) -> bool:
        gpu = self.sucheGrafikkarte(artikelNr)

        if gpu and gpu.getBestand() >= menge:
            neuer_bestand = gpu.getBestand() - menge
            erloes = gpu.getVerkaufspreis() * menge

            db = DatabaseManager()

            db.execute_query("UPDATE Grafikkarte SET bestand = %s WHERE artikelNr = %s", (neuer_bestand, artikelNr))

            self.setBudget(self.getBudget() + erloes)
            self.setUmsatz(self.getUmsatz() + erloes)

            self.shop_finanzen_speichern()

            self.daten_laden()
            return True
        return False

    def addGrafikkarte(self, modell, hersteller, marke, vramGroesse, speichertyp, einkaufspreis, verkaufspreis) -> bool:
        db = DatabaseManager()
        query = """INSERT INTO Grafikkarte 
                   (modell, hersteller, marke, vramGroesse, speichertyp, einkaufspreis, verkaufspreis, bestand, shopID) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (modell, hersteller, marke, vramGroesse, speichertyp, einkaufspreis, verkaufspreis, 0, self.getShopID())
        erfolg = db.execute_query(query, params)
        if erfolg:
            self.daten_laden()
        return erfolg

    def sucheGrafikkarte(self, artikelNr) -> Grafikkarte:
        for gpu in self.getAlleGrafikkarten():
            if str(gpu.getArtikelNr()) == str(artikelNr):
                return gpu
        return None

    def getAlleGrafikkarten(self):
        return self.__alleGrafikkarten
    
    def removeGrafikkarte(self, artikelNr) -> bool:
        db = DatabaseManager()
        query = "DELETE FROM Grafikkarte WHERE artikelNr = %s"
        erfolg = db.execute_query(query, (artikelNr,))
        if erfolg:
            self.daten_laden()
        return erfolg

    @staticmethod
    def main():
        gpushop1 = Grafikkartenshop(1)
        root = tk.Tk()
        root.title(f"Verwaltung: {gpushop1.getName()}")
        root.withdraw()
        main_container = tk.Frame(root)
        main_container.pack(fill="both", expand=True)

        def clear_container():
            for widget in main_container.winfo_children():
                widget.destroy()

        def zeige_hauptmenue():
            clear_container()
            root.geometry("400x500")
            tk.Label(main_container, text="HAUPTMENÜ", font=("Arial", 16, "bold")).pack(pady=20)

            buttons = [
                ("Bestand anzeigen", zeige_tabelle),
                ("Grafikkarte suchen", zeige_suche),
                ("Grafikkarte hinzufügen", zeige_hinzufuegen),
                ("Löschen", zeige_loeschen),
                ("Einkaufen / Verkaufen", zeige_handel)
            ]

            for text, cmd in buttons:
                tk.Button(main_container, text=text, command=cmd, width=25, pady=5).pack(pady=5)

        def zeige_tabelle():
            
            clear_container()

            root.geometry("1100x600")

            tk.Button(main_container, text="Zurück", command=zeige_hauptmenue).pack(anchor="w", padx=10, pady=5)

            table_frame = tk.Frame(main_container)
            table_frame.pack(fill="both", expand=True, padx=20, pady=10)

            scrollbar = tk.Scrollbar(table_frame, orient="vertical")
            scrollbar.pack(side="right", fill="y")

            # Tabelle erstellen
            columns = ("Artikelnummer", "Modell", "Hersteller", "Marke", "VRAM-Groesse", "Speichertyp", "Einkaufspreis", "Verkaufspreis", "Bestand")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)

            scrollbar.config(command=tree.yview)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=110, anchor="center")

            # Daten über den Getter holen und einfügen
            for gpu in gpushop1.getAlleGrafikkarten():
                tree.insert("", tk.END, values=(
                    gpu.getArtikelNr(),
                    gpu.getModell(),
                    gpu.getHersteller(),
                    gpu.getMarke(),
                    gpu.getVramGroesse(),
                    gpu.getSpeichertyp(),
                    f"{gpu.getEinkaufspreis():.2f} €",
                    f"{gpu.getVerkaufspreis():.2f} €",
                    gpu.getBestand()
                ))

            tree.pack(side="left", fill="both", expand=True)

        def zeige_suche():
            clear_container()
            root.geometry("500x300")
            tk.Button(main_container, text="Zurück", command=zeige_hauptmenue).pack(anchor="w", padx=10)
            tk.Label(main_container, text="Nach Grafikkarte anhand der Artikelnummer suchen", font=("Arial", 14)).pack(pady=10)
            ent_nr = tk.Entry(main_container)
            ent_nr.pack(pady=5)

            lbl_result = tk.Label(main_container, text="", justify="left")
            lbl_result.pack(pady=10)

            def start_suche():
                nr = ent_nr.get()
                gpu = gpushop1.sucheGrafikkarte(nr)
                if gpu:
                    res = f"Artikelnummer: {gpu.getArtikelNr()}\nModell: {gpu.getModell()}\nHersteller: {gpu.getHersteller()}\nMarke: {gpu.getMarke()}\nVRAM-Groesse: {gpu.getVramGroesse()}\nSpeichertyp: {gpu.getSpeichertyp()}\nEinkaufspreis: {gpu.getEinkaufspreis()}\nVerkaufspreis: {gpu.getVerkaufspreis()}\nBestand: {gpu.getBestand()}\n"
                    lbl_result.config(text=res, fg="black")
                else:
                    lbl_result.config(text="Keine Grafikkarte gefunden!", fg="red")
            
            tk.Button(main_container, text="Suchen", command=start_suche).pack()

        def zeige_hinzufuegen():
            clear_container()
            root.geometry("500x600")
            tk.Button(main_container, text="Zurück", command=zeige_hauptmenue).pack(anchor="w", padx=10, pady=5)
            tk.Label(main_container, text="Neue Grafikkarte hinzufügen", font=("Arial", 14, "bold")).pack(pady=10)

            felder = ["Modell", "Hersteller", "Marke", "VRAM-Groesse (GB)", "Speichertyp", "Einkaufspreis", "Verkaufspreis"]

            entries = {}

            for feld in felder:
                frame = tk.Frame(main_container)
                frame.pack(fill="x", padx=50, pady=5)
                tk.Label(frame, text=feld, width=15, anchor="w").pack(side="left")
                en = tk.Entry(frame)
                en.pack(side="right", expand=True, fill="x")
                entries[feld] = en
            
            def speichern():
                try:
                    erfolg = gpushop1.addGrafikkarte(
                        entries["Modell"].get(),
                        entries["Hersteller"].get(),
                        entries["Marke"].get(),
                        int(entries["VRAM-Groesse (GB)"].get()),
                        entries["Speichertyp"].get(),
                        float(entries["Einkaufspreis"].get()),
                        float(entries["Verkaufspreis"].get())
                    )

                    if erfolg:
                        messagebox.showinfo("Erfolg", "Grafikkarte wurde erfolgreich gespeichert!")
                        zeige_hauptmenue()
                except ValueError:
                    messagebox.showinfo("Fehler", "Bitte bei Preisen und VRAM nur Zahlen eingeben!")

            tk.Button(main_container, text="In Datenbank speichern", command=speichern, bg="green", fg="white", pady=10).pack(pady=20)

        def zeige_loeschen():
            clear_container()
            root.geometry("450x300")
            tk.Button(main_container, text="Zurück", command=zeige_hauptmenue).pack(anchor="w", padx=10, pady=5)
            tk.Label(main_container, text="Grafikkarte löschen", font=("Arial", 14, "bold"), fg="red").pack(pady=10)
            tk.Label(main_container, text="Geben Sie die Artikelnummer ein:").pack(pady=5)
            ent_nr = tk.Entry(main_container, width=15)
            ent_nr.pack(pady=5)

            def loesch_vorgang():
                nr = ent_nr.get()
                if not nr:
                    return
                
                gpu = gpushop1.sucheGrafikkarte(nr)
                if gpu:
                    bestaetigung = messagebox.askyesno("Löschen bestätigen", f"Möchten Sie die Grafikkarte '{gpu.getModell()}' (Art-Nr: {nr}) wirklich unwiderruflich löschen?")

                    if bestaetigung:
                        if gpushop1.removeGrafikkarte(nr):
                            messagebox.showinfo("Erfolg", "Grafikkarte wurde erfolgreich gelöscht!")
                            zeige_hauptmenue()
                else:
                    messagebox.showerror("Fehler", f"Keine Grafikkarte mit der Nummer {nr} gefunden.")
            
            tk.Button(main_container, text="Datensatz löschen", command=loesch_vorgang, bg="red", fg="white").pack(pady=20)

        def zeige_handel():
            clear_container()
            root.geometry("500x450")
            tk.Button(main_container, text="Zurück", command=zeige_hauptmenue).pack(anchor="w", padx=10, pady=5)

            finanz_frame = tk.LabelFrame(main_container, text=" Shop Finanzen ", padx=10, pady=10)
            finanz_frame.pack(fill="x", padx=20, pady=10)

            tk.Label(finanz_frame, text=f"Aktuelles Budget: {gpushop1.getBudget():.2f} €", fg="green", font=("Arial", 10, "bold")).pack(side="left", padx=10)
            tk.Label(finanz_frame, text=f"Gesamtumsatz: {gpushop1.getUmsatz():.2f} €", fg="blue", font=("Arial", 10, "bold")).pack(side="right", padx=10)

            tk.Label(main_container, text="Grafikkarte VERKAUFEN", font=("Arial", 14, "bold")).pack(pady=10)

            tk.Label(main_container, text="Artikelnummer:").pack()
            ent_nr = tk.Entry(main_container)
            ent_nr.pack()

            tk.Label(main_container, text="Menge:").pack()
            ent_menge = tk.Entry(main_container)
            ent_menge.pack()

            def ausfuehren_verkauf():
                try:
                    nr = ent_nr.get()
                    menge = int(ent_menge.get())

                    if gpushop1.grafikkarteVerkaufen(nr, menge):
                        messagebox.showinfo("Erfolg", f"Verkauf abgeschlossen!\nUmsatz generiert: +{gpushop1.sucheGrafikkarte(nr).getVerkaufspreis() * menge:.2f} €")
                        zeige_handel()
                    else:
                        messagebox.showerror("Fehler", "Verkauf nicht möglich (Bestand zu niedrig oder Art-Nr falsch).")
                except ValueError:
                    messagebox.showerror("Fehler", "Bitte eine gültige Menge (Zahl) eingeben.")

            tk.Button(main_container, text="Verkauf bestätigen", command=ausfuehren_verkauf, bg="blue", fg="white", pady=5).pack(pady=20)

            tk.Canvas(main_container, height=2, bg="gray").pack(fill="x", pady=20)

            tk.Label(main_container, text="Grafikkarte EINKAUFEN", font=("Arial", 14, "bold"), fg="darkgreen").pack(pady=10)

            tk.Label(main_container, text="Artikelnummer:").pack()
            ent_nr_ek = tk.Entry(main_container)
            ent_nr_ek.pack()

            tk.Label(main_container, text="Menge:").pack()
            ent_menge_ek = tk.Entry(main_container)
            ent_menge_ek.pack()

            def ausfuehren_einkauf():
                try:
                    nr = ent_nr_ek.get()
                    menge = int(ent_menge_ek.get())

                    if gpushop1.grafikkarteEinkaufen(nr, menge):
                        messagebox.showinfo("Erfolg", "Einkauf erfolgreich gebucht!")
                        zeige_handel()
                    else:
                        messagebox.showerror("Fehler", "Nicht genug Kapital verfügbar (Budget + Umsatz zu niedrig)")
                except ValueError:
                    messagebox.showerror("Fehler", "Bitte eine gültige Menge (Zahl) eingeben.")
                
            tk.Button(main_container, text="Einkauf bestätigen", command=ausfuehren_einkauf, bg="green", fg="white", pady=5).pack(pady=20)

        def zeige_begruessung():
            
            clear_container()

            root.geometry("800x450")

            tk.Label(main_container, text=f"Willkommen im {gpushop1.getName()}", font=("Arial", 18)).pack(pady=50)
            tk.Button(main_container, text="Programm starten", command=zeige_hauptmenue).pack()

        def zeige_ladescreen():

            clear_container()

            try:
                img = Image.open("auragpustartscreen.jpg")
                original_breite, original_hoehe = img.size
                neue_breite = 275
                verhaeltnis = original_hoehe / original_breite
                neue_hoehe = int(neue_breite * verhaeltnis)
                img = img.resize((neue_breite, neue_hoehe), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)

                root.geometry(f"{neue_breite}x{neue_hoehe}")

                root.deiconify()
                root.update()

                lbl = tk.Label(main_container, image=img_tk)
                lbl.image = img_tk
                lbl.pack()
            except Exception as e:
                print(f"Ladescreen Fehler: {e}")
                root.geometry("400x200")
                root.deiconify()
                tk.Label(main_container, text="Lade...").pack(expand=True)

            root.after(3000, zeige_begruessung)

        zeige_ladescreen()

        root.mainloop()

Grafikkartenshop.main()
