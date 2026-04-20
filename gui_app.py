import tkinter as tk
from tkinter import messagebox, ttk
from database import DatabaseManager
from gpu_handel import GPUHandel

class GPUApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPU Bestandsführung Pro - Admin-Panel")
        self.root.geometry("700x700")

        # Datenbank-Initialisierung (Passwort leer für Standard-XAMPP)
        self.db = DatabaseManager("localhost", "root", "", "gpu_shop")
        self.handel = GPUHandel(self.db)

        self._setup_ui()

    def _setup_ui(self):
        # --- BEREICH 1: Neuen Artikel registrieren ---
        frame_add = tk.LabelFrame(self.root, text="Neuen Artikel registrieren", padx=10, pady=10, fg="blue")
        frame_add.pack(fill="x", padx=20, pady=10)

        # Gitter-Layout für das Registrier-Formular
        labels = ["ID (z.B. RTX4070):", "Name:", "EK-Preis (€):", "VK-Preis (€):", "Mindestbestand:"]
        self.add_entries = {}

        for i, label in enumerate(labels):
            tk.Label(frame_add, text=label).grid(row=i, column=0, sticky="w", pady=2)
            entry = tk.Entry(frame_add)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
            self.add_entries[label] = entry

        btn_register = tk.Button(frame_add, text="Artikel in Datenbank speichern",
                                 command=self.handle_registration, bg="#007bff", fg="white")
        btn_register.grid(row=len(labels), column=0, columnspan=2, pady=10, sticky="ew")


        # --- BEREICH 2: Bestandsführung (Wareneingang/Verkauf) ---
        frame_action = tk.LabelFrame(self.root, text="Lager-Aktionen (Eingang/Verkauf)", padx=10, pady=10, fg="green")
        frame_action.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_action, text="GPU ID:").grid(row=0, column=0, sticky="w")
        self.ent_action_id = tk.Entry(frame_action)
        self.ent_action_id.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_action, text="Menge:").grid(row=1, column=0, sticky="w")
        self.ent_menge = tk.Entry(frame_action)
        self.ent_menge.grid(row=1, column=1, padx=5, pady=2)

        btn_we = tk.Button(frame_action, text="Wareneingang", command=self.handle_we, bg="#d4edda")
        btn_we.grid(row=0, column=2, padx=10, sticky="ew")

        btn_vk = tk.Button(frame_action, text="Verkauf", command=self.handle_vk, bg="#f8d7da")
        btn_vk.grid(row=1, column=2, padx=10, sticky="ew")


        # --- BEREICH 3: Log / Anzeige ---
        frame_display = tk.LabelFrame(self.root, text="Protokoll", padx=10, pady=10)
        frame_display.pack(fill="both", expand=True, padx=20, pady=10)

        self.txt_log = tk.Text(frame_display, height=8, state="disabled", bg="#f8f9fa")
        self.txt_log.pack(fill="both", expand=True)

        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=5)

    def log(self, message):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", message + "\n")
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

    def handle_registration(self):
        """Liest die Daten für eine neue GPU aus und speichert sie."""
        try:
            gpu_id = self.add_entries["ID (z.B. RTX4070):"].get()
            name = self.add_entries["Name:"].get()
            ek = float(self.add_entries["EK-Preis (€):"].get())
            vk = float(self.add_entries["VK-Preis (€):"].get())
            min_bst = int(self.add_entries["Mindestbestand:"].get())

            if not gpu_id or not name:
                raise ValueError("ID und Name dürfen nicht leer sein.")

            self.handel.neuen_artikel_registrieren(gpu_id, name, ek, vk, min_bst)
            self.log(f"NEU ANGELEGT: {name} (ID: {gpu_id})")
            messagebox.showinfo("Erfolg", f"Artikel {name} wurde registriert.")

            # Felder leeren
            for entry in self.add_entries.values():
                entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Eingabefehler", f"Bitte korrekte Daten eingeben!\nFehler: {e}")

    def handle_we(self):
        gpu_id = self.ent_action_id.get()
        try:
            menge = int(self.ent_menge.get())
            self.handel.wareneingang(gpu_id, menge)
            self.log(f"WARENEINGANG: {menge}x für ID {gpu_id}")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def handle_vk(self):
        gpu_id = self.ent_action_id.get()
        try:
            menge = int(self.ent_menge.get())
            # Die Logik für Umsatz/Gewinn ist bereits in gpu_handel.py
            self.handel.verkauf_abwickeln(gpu_id, menge)
            self.log(f"VERKAUF ABGEWICKELT: {menge}x für ID {gpu_id}")
        except Exception as e:
            messagebox.showerror("Fehler!", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = GPUApp(root)
    root.mainloop()