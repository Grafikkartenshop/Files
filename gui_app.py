import tkinter as tk
from tkinter import messagebox, ttk
from database import DatabaseManager
from gpu_handel import GPUHandel

class GPUApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPU Bestandsführung Pro - Admin-Panel")
        self.root.geometry("850x950")

        # Datenbank-Initialisierung
        self.db = DatabaseManager("localhost", "root", "", "gpu_shop")
        self.handel = GPUHandel(self.db)

        self._setup_ui()
        self.refresh_table()

    def _setup_ui(self):
        # --- BEREICH 1: Tabelle ---
        frame_table = tk.LabelFrame(self.root, text="Aktueller Bestand", padx=10, pady=10)
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("id", "name", "ek", "vk", "bestand")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")

        self.tree.heading("id", text="GPU ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("ek", text="EK-Preis")
        self.tree.heading("vk", text="VK-Preis")
        self.tree.heading("bestand", text="Bestand")

        for col in columns:
            self.tree.column(col, width=120)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # --- NEU: FINANZ-ANZEIGE ---
        self.frame_stats = tk.Frame(self.root, pady=5)
        self.frame_stats.pack(fill="x", padx=25)

        self.lbl_umsatz = tk.Label(self.frame_stats, text="Umsatz: 0.00 €", font=("Arial", 11, "bold"), fg="#333")
        self.lbl_umsatz.pack(side="left", padx=20)

        self.lbl_gewinn = tk.Label(self.frame_stats, text="Gewinn: 0.00 €", font=("Arial", 11, "bold"), fg="green")
        self.lbl_gewinn.pack(side="left", padx=20)

        # --- BEREICH 2: Registrierung ---
        frame_add = tk.LabelFrame(self.root, text="Artikel-Details", padx=10, pady=10, fg="blue")
        frame_add.pack(fill="x", padx=20, pady=10)

        labels = ["ID (z.B. RTX4070):", "Name:", "EK-Preis (€):", "VK-Preis (€):", "Mindestbestand:"]
        self.add_entries = {}

        for i, label in enumerate(labels):
            tk.Label(frame_add, text=label).grid(row=i, column=0, sticky="w", pady=2)
            entry = tk.Entry(frame_add)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
            self.add_entries[label] = entry

        btn_register = tk.Button(frame_add, text="Neu anlegen / Speichern",
                                 command=self.handle_registration, bg="#007bff", fg="white")
        btn_register.grid(row=len(labels), column=0, columnspan=2, pady=10, sticky="ew")

        # --- BEREICH 3: Aktionen ---
        frame_action = tk.LabelFrame(self.root, text="Aktionen für ausgewählte GPU", padx=10, pady=10, fg="green")
        frame_action.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_action, text="Ausgewählte ID:").grid(row=0, column=0, sticky="w")
        self.ent_action_id = tk.Entry(frame_action, state="readonly", readonlybackground="#e9ecef")
        self.ent_action_id.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_action, text="Menge:").grid(row=1, column=0, sticky="w")
        self.ent_menge = tk.Entry(frame_action)
        self.ent_menge.grid(row=1, column=1, padx=5, pady=2)

        btn_we = tk.Button(frame_action, text="Wareneingang", command=self.handle_we, bg="#d4edda", width=15)
        btn_we.grid(row=0, column=2, padx=5, pady=2)

        btn_vk = tk.Button(frame_action, text="Verkauf", command=self.handle_vk, bg="#f8d7da", width=15)
        btn_vk.grid(row=1, column=2, padx=5, pady=2)

        btn_del = tk.Button(frame_action, text="Löschen", command=self.handle_deletion, bg="#dc3545", fg="white", width=15)
        btn_del.grid(row=0, column=3, padx=5, pady=2)

        # --- BEREICH 4: Log ---
        self.txt_log = tk.Text(self.root, height=5, state="disabled", bg="#f8f9fa")
        self.txt_log.pack(fill="x", padx=20, pady=10)

    def refresh_table(self):
        """Aktualisiert Tabelle und Finanzwerte."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 1. Tabelle füllen
        daten = self.handel.get_alle_artikel()
        for row in daten:
            self.tree.insert("", "end", values=row)

        # 2. Finanzen berechnen (über die neue sales-Tabelle in der DB)
        umsatz, gewinn = self.handel.get_finanzen()

        # Labels aktualisieren
        self.lbl_umsatz.config(text=f"Gesamtumsatz: {float(umsatz):.2f} €")
        self.lbl_gewinn.config(text=f"Gesamtgewinn: {float(gewinn):.2f} €")

        # Farbe bei Verlust auf Rot setzen
        self.lbl_gewinn.config(fg="red" if gewinn < 0 else "green")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)["values"]
            self.ent_action_id.config(state="normal")
            self.ent_action_id.delete(0, tk.END)
            self.ent_action_id.insert(0, values[0])
            self.ent_action_id.config(state="readonly")

    def log(self, message):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", message + "\n")
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

    def handle_registration(self):
        try:
            gpu_id = self.add_entries["ID (z.B. RTX4070):"].get()
            name = self.add_entries["Name:"].get()
            ek = float(self.add_entries["EK-Preis (€):"].get())
            vk = float(self.add_entries["VK-Preis (€):"].get())
            min_bst = int(self.add_entries["Mindestbestand:"].get())
            self.handel.neuen_artikel_registrieren(gpu_id, name, ek, vk, min_bst)
            self.refresh_table()
            messagebox.showinfo("Erfolg", "Artikel gespeichert.")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def handle_deletion(self):
        gpu_id = self.ent_action_id.get()
        if not gpu_id: return
        if messagebox.askyesno("Löschen", f"ID {gpu_id} wirklich löschen?"):
            self.handel.artikel_loeschen(gpu_id)
            self.refresh_table()
            self.log(f"GELÖSCHT: {gpu_id}")

    def handle_we(self):
        gpu_id = self.ent_action_id.get()
        try:
            menge = int(self.ent_menge.get())
            self.handel.wareneingang(gpu_id, menge)
            self.refresh_table()
            self.log(f"WARENEINGANG: {menge}x für {gpu_id}")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def handle_vk(self):
        gpu_id = self.ent_action_id.get()
        try:
            menge = int(self.ent_menge.get())
            self.handel.verkauf_abwickeln(gpu_id, menge)
            self.refresh_table()
            self.log(f"VERKAUF: {menge}x für {gpu_id}")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = GPUApp(root)
    root.mainloop()