import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

from file_sorter_core import file_sort, normalize_input_path


class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FileSorter")
        self.root.geometry("560x250")
        self.root.resizable(False, False)

        self.path_var = tk.StringVar()

        container = tk.Frame(self.root, padx=16, pady=16)
        container.pack(fill="both", expand=True)

        title = tk.Label(container, text="Ordner sortieren", font=("Segoe UI", 13, "bold"))
        title.pack(anchor="w")

        subtitle = tk.Label(container, text="Pfad einfügen oder per Drag & Drop auswählen")
        subtitle.pack(anchor="w", pady=(2, 12))

        path_frame = tk.Frame(container)
        path_frame.pack(fill="x")

        path_entry = tk.Entry(path_frame, textvariable=self.path_var)
        path_entry.pack(side="left", fill="x", expand=True)

        browse_button = tk.Button(path_frame, text="Ordner wählen", command=self.choose_folder)
        browse_button.pack(side="left", padx=(8, 0))

        self.drop_label = tk.Label(
            container,
            text="Ordner hier hineinziehen",
            relief="groove",
            borderwidth=2,
            height=5
        )
        self.drop_label.pack(fill="x", pady=(12, 12))
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self.on_drop)

        sort_button = tk.Button(container, text="Sortieren", command=self.sort_files)
        sort_button.pack(anchor="e")

    def choose_folder(self):
        selected = filedialog.askdirectory()
        if selected:
            self.path_var.set(selected)

    def on_drop(self, event):
        dropped_items = self.root.tk.splitlist(event.data)
        if not dropped_items:
            return

        dropped_path = normalize_input_path(dropped_items[0])
        self.path_var.set(str(dropped_path))

    def sort_files(self):
        try:
            moved_count = file_sort(self.path_var.get())
            messagebox.showinfo("Fertig", f"Sortieren abgeschlossen. Verschoben: {moved_count}")
        except Exception as error:
            messagebox.showerror("Fehler", str(error))


def run_gui():
    root = TkinterDnD.Tk()
    FileSorterApp(root)
    root.mainloop()