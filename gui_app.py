import tkinter as tk
from tkinter import messagebox, ttk
from database import DatabaseManager
from gpu_handel import GPUHandel

class GPUApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPU Management System")
        self.root.geometry("800x750")

        # Datenbank-Verbindung (XAMPP Standard)
        self.db = DatabaseManager("localhost", "root", "", "gpu_shop")
        self.handel = GPUHandel(self.db)

        self._setup_ui()
        self.refresh_table()

    def _setup_ui(self):
        # 1. Tabelle
        frame_table = tk.LabelFrame(self.root, text="Lagerbestand", padx=10, pady=10)
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("id", "name", "ek", "vk", "bestand")
        self.tree = ttk.Treeview(frame_table, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # 2. Registrierung
        frame_add = tk.LabelFrame(self.root, text="Artikel anlegen", padx=10, pady=10)
        frame_add.pack(fill="x", padx=20, pady=5)

        self.entries = {}
        labels = ["ID", "Name", "EK", "VK", "Mindestbestand"]
        for i, label in enumerate(labels):
            tk.Label(frame_add, text=label).grid(row=i, column=0, sticky="w")
            e = tk.Entry(frame_add)
            e.grid(row=i, column=1, sticky="ew", padx=5)
            self.entries[label] = e

        tk.Button(frame_add, text="Speichern", command=self.handle_add, bg="blue", fg="white").grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)

        # 3. Aktionen
        frame_act = tk.LabelFrame(self.root, text="Aktionen", padx=10, pady=10)
        frame_act.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_act, text="ID:").grid(row=0, column=0)
        self.lbl_sel_id = tk.Entry(frame_act, state="readonly")
        self.lbl_sel_id.grid(row=0, column=1, padx=5)

        tk.Label(frame_act, text="Menge:").grid(row=0, column=2)
        self.ent_menge = tk.Entry(frame_act, width=10)
        self.ent_menge.grid(row=0, column=3, padx=5)

        tk.Button(frame_act, text="Eingang", command=self.handle_we, bg="green", fg="white").grid(row=0, column=4, padx=5)
        tk.Button(frame_act, text="Verkauf", command=self.handle_vk, bg="orange").grid(row=0, column=5, padx=5)
        tk.Button(frame_act, text="Löschen", command=self.handle_del, bg="red", fg="white").grid(row=0, column=6, padx=5)

        # 4. Log
        self.txt_log = tk.Text(self.root, height=5, state="disabled")
        self.txt_log.pack(fill="x", padx=20, pady=10)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.handel.get_alle_artikel():
            self.tree.insert("", "end", values=row)

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if sel:
            val = self.tree.item(sel)["values"]
            self.lbl_sel_id.config(state="normal")
            self.lbl_sel_id.delete(0, tk.END)
            self.lbl_sel_id.insert(0, val[0])
            self.lbl_sel_id.config(state="readonly")

    def log(self, msg):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", msg + "\n")
        self.txt_log.config(state="disabled")

    def handle_add(self):
        try:
            self.handel.neuen_artikel_registrieren(
                self.entries["ID"].get(), self.entries["Name"].get(),
                float(self.entries["EK"].get()), float(self.entries["VK"].get()),
                int(self.entries["Mindestbestand"].get())
            )
            self.refresh_table()
            messagebox.showinfo("Erfolg", "Artikel angelegt")
        except Exception as e: messagebox.showerror("Fehler", str(e))

    def handle_we(self):
        try:
            self.handel.wareneingang(self.lbl_sel_id.get(), int(self.ent_menge.get()))
            self.refresh_table()
            self.log(f"Eingang: {self.ent_menge.get()}x {self.lbl_sel_id.get()}")
        except Exception as e: messagebox.showerror("Fehler", str(e))

    def handle_vk(self):
        try:
            self.handel.verkauf_abwickeln(self.lbl_sel_id.get(), int(self.ent_menge.get()))
            self.refresh_table()
            self.log(f"Verkauf: {self.ent_menge.get()}x {self.lbl_sel_id.get()}")
        except Exception as e: messagebox.showerror("Fehler", str(e))

    def handle_del(self):
        if messagebox.askyesno("Löschen", "Sicher?"):
            self.handel.artikel_loeschen(self.lbl_sel_id.get())
            self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = GPUApp(root)
    root.mainloop()