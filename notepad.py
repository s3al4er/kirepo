import tkinter as tk
from tkinter import scrolledtext, ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog

class SimpleNotepad:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Notepad")

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def create_menu(self):
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Select All", command=self.select_all)
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.master.config(menu=menubar)

        # Binding keyboard shortcuts
        self.master.bind_all("<Control-c>", lambda event: self.copy())
        self.master.bind_all("<Control-v>", lambda event: self.paste())

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))

    def quit_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.master.destroy()

    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)

    def copy(self):
        self.text_area.clipboard_clear()
        self.text_area.clipboard_append(self.text_area.selection_get())

    def paste(self):
        self.text_area.insert(tk.INSERT, self.text_area.clipboard_get())

def main():
    root = tk.Tk()
    app = SimpleNotepad(root)
    root.mainloop()

if __name__ == "__main__":
    main()