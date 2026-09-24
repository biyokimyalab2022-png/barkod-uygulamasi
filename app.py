import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "barkod_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class BarkodApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Barkod Mesaj Sistemi - Argox CP-3140")
        self.root.geometry("600x500")
        self.data = load_data()

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_scan = ttk.Frame(notebook)
        self.tab_manage = ttk.Frame(notebook)

        notebook.add(self.tab_scan, text=" Barkod Okut ")
        notebook.add(self.tab_manage, text=" Barkod / Cümle Tanımla ")

        self.setup_scan_tab()
        self.setup_manage_tab()

    def setup_scan_tab(self):
        lbl = ttk.Label(self.tab_scan, text="Barkod Okutun:", font=("Arial", 12, "bold"))
        lbl.pack(pady=(20, 5))

        self.entry_barcode = ttk.Entry(self.tab_scan, font=("Arial", 14))
        self.entry_barcode.pack(fill="x", padx=30, pady=5)
        self.entry_barcode.focus()
        self.entry_barcode.bind("<Return>", self.on_barcode_scan)

        self.lbl_result = tk.Label(
            self.tab_scan, 
            text="Lütfen bir barkod okutun...", 
            font=("Arial", 14, "bold"), 
            wraplength=500, 
            bg="#f0f0f0", 
            relief="groove", 
            padx=10, 
            pady=20
        )
        self.lbl_result.pack(fill="both", expand=True, padx=30, pady=20)

    def on_barcode_scan(self, event):
        code = self.entry_barcode.get().strip()
        self.entry_barcode.delete(0, tk.END)

        if code in self.data:
            self.lbl_result.config(text=self.data[code], bg="#d4edda", fg="#155724")
        else:
            self.lbl_result.config(text=f"'{code}' koduna ait mesaj bulunamadı!", bg="#f8d7da", fg="#721c24")

    def setup_manage_tab(self):
        frame_inputs = ttk.Frame(self.tab_manage)
        frame_inputs.pack(fill="x", padx=20, pady=10)

        ttk.Label(frame_inputs, text="Barkod No (Örn: 10001):").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_key = ttk.Entry(frame_inputs, width=30)
        self.entry_key.grid(row=0, column=1, sticky="w", pady=5)

        ttk.Label(frame_inputs, text="Cümle / Mesaj:").grid(row=1, column=0, sticky="nw", pady=5)
        self.txt_val = tk.Text(frame_inputs, width=35, height=4)
        self.txt_val.grid(row=1, column=1, sticky="w", pady=5)

        btn_save = ttk.Button(frame_inputs, text="Kaydet / Güncelle", command=self.save_entry)
        btn_save.grid(row=2, column=1, sticky="e", pady=10)

        self.tree = ttk.Treeview(self.tab_manage, columns=("Barkod", "Mesaj"), show="headings")
        self.tree.heading("Barkod", text="Barkod No")
        self.tree.heading("Mesaj", text="Tanımlı Mesaj")
        self.tree.column("Barkod", width=120)
        self.tree.column("Mesaj", width=350)
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.update_list()

    def save_entry(self):
        key = self.entry_key.get().strip()
        val = self.txt_val.get("1.0", tk.END).strip()

        if not key or not val:
            messagebox.showwarning("Uyarı", "Lütfen hem barkod numarasını hem de cümleyi girin.")
            return

        self.data[key] = val
        save_data(self.data)
        self.update_list()
        self.entry_key.delete(0, tk.END)
        self.txt_val.delete("1.0", tk.END)
        messagebox.showinfo("Başarılı", "Barkod başarıyla kaydedildi!")

    def update_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for k, v in self.data.items():
            self.tree.insert("", tk.END, values=(k, v))

if __name__ == "__main__":
    root = tk.Tk()
    app = BarkodApp(root)
    root.mainloop()