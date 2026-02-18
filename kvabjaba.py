import tkinter as tk
from tkinter import messagebox, filedialog


class TextEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tkinter Text Editor")
        self.geometry("800x600")

        self.current_file = None

        self._create_menu()
        self._create_text_area()
        self._bind_shortcuts()

    # ================= MENU =================
    def _create_menu(self):
        menu_bar = tk.Menu(self)

        # -------- File Menu --------
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # -------- Edit Menu --------
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all)

        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.config(menu=menu_bar)

    # ================= TEXT AREA =================
    def _create_text_area(self):
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = tk.Text(
            frame,
            wrap=tk.WORD,
            undo=True,
            font=("Consolas", 12)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=scrollbar.set)

    # ================= SHORTCUTS =================
    def _bind_shortcuts(self):
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-a>", lambda e: self.select_all())
        self.bind("<Control-z>", lambda e: self.undo())
        self.bind("<Control-y>", lambda e: self.redo())

    # ================= EDIT FUNCTIONS =================
    def undo(self):
        try:
            self.text_area.edit_undo()
        except:
            pass

    def redo(self):
        try:
            self.text_area.edit_redo()
        except:
            pass

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def select_all(self):
        self.text_area.tag_add("sel", "1.0", tk.END)
        return "break"

    # ================= FILE FUNCTIONS =================
    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, content)

            self.current_file = file_path
            self.title(f"Tkinter Text Editor - {file_path}")

    def save_file(self):
        if not self.current_file:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if not file_path:
                return
            self.current_file = file_path
        else:
            file_path = self.current_file

        with open(file_path, "w", encoding="utf-8") as file:
            content = self.text_area.get("1.0", tk.END)
            file.write(content)

        self.title(f"Tkinter Text Editor - {file_path}")

    # ================= EXIT =================
    def exit_application(self):
        if messagebox.askyesno("გასვლა", "ნამდვილად გსურთ პროგრამიდან გასვლა?"):
            self.destroy()


if __name__ == "__main__":
    app = TextEditor()
    app.mainloop()
