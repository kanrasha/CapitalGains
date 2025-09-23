# noinspection SpellCheckingInspection
"""
Features:
- Dropdown for FIFO / LIFO / HIFO
- 'Run' button triggers capgains
- 'Checksum' button triggers checksum
- Uses existing constants and functions unchanged.

TO DO:
- the GUI prints 'Imports Formatted' twice, so something is inefficient here, but works fine
"""

import tkinter as tk
import file_prep0_3; file_prep0_3.run()
from tkinter import messagebox
from pathlib import Path
from CapGains4_2 import capgains, checksum
import io, sys

ROOT = Path(__file__).parent

class CapGainsGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.attributes("-fullscreen", True)  # Helpful for testing
        self.title("Cap-Gains 4.2 GUI")
        self.geometry("800x400")
        self.method_var = tk.StringVar(value="Run All Methods")

        tk.Label(self, text="Method:").pack(pady=5)
        tk.OptionMenu(self, self.method_var, "Run All Methods","FIFO", "LIFO", "HIFO").pack()

        tk.Button(self, text="Run", command=self.run).pack(pady=10)
        tk.Button(self, text="Checksum", command=self.check).pack(pady=5)

    def show_output_window(self, output_text):
        win = tk.Toplevel(self)
        win.title("Output")
        # Position the window below the main GUI
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_height = self.winfo_height()
        win.geometry(f"800x200+{main_x}+{main_y + main_height + 10}")  # 10px below main window
        win.lower(self)  # Send printout window behind main window

        text_widget = tk.Text(win, wrap="word", width=100, height=20, font=("Menlo", 14))
        text_widget.pack(expand=True, fill="both")
        text_widget.insert("end", output_text)
        text_widget.config(state="disabled")

    def run(self):
        method = self.method_var.get()
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            if method == "Run All Methods":
                capgains("fifo")
                capgains("lifo")
                capgains("hifo")
            else:
                capgains(method)
        finally:
            sys.stdout = old_stdout
        output = buffer.getvalue()
        self.show_output_window(output)
        messagebox.showinfo("Done", f"Finished {method.upper()} processing.")

    def check(self):
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            checksum()
        finally:
            sys.stdout = old_stdout
        output = buffer.getvalue()
        self.show_output_window(output)
        messagebox.showinfo("Checksum", "Checksum completed.")

if __name__ == "__main__":
    CapGainsGUI().mainloop()


'''
tkinter is not easily installable on pycharm, but it is python3 built-in 
<https://intellij-support.jetbrains.com/hc/en-us/community/posts/360010719620-No-tkinter-in-pycharm>

`tkinter` python module is just bindings for Tk, which you must have installed separately on your system. 
A comprehensive guide can be found here: <https://tkdocs.com/tutorial/install.html>
'''