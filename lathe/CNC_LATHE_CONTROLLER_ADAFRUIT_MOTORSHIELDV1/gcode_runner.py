import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import time

class GCodeRunner:
    def __init__(self, app):
        self.app = app
        self.gcode_content = ""

    def preview_gcode(self):
        self.gcode_file_path = filedialog.askopenfilename(filetypes=[("G-code Files", "*.gcode"), ("Text Files", "*.txt")])
        if self.gcode_file_path:
            with open(self.gcode_file_path, "r") as file:
                self.gcode_content = file.read()

            preview_window = tk.Toplevel(self.app.root)
            preview_window.title("G-code Preview")
            text_area = scrolledtext.ScrolledText(preview_window, width=60, height=20)
            text_area.pack()
            text_area.insert(tk.END, self.gcode_content)
            
            run_button = tk.Button(preview_window, text="Run G-code", command=self.run_gcode)
            run_button.pack()

    def run_gcode(self):
        if not self.app.serial_control.serial_port:
            messagebox.showerror("Error", "Not connected to any port")
            return

        if self.gcode_content:
            for line in self.gcode_content.splitlines():
                if line.strip():
                    self.app.serial_control.serial_port.write(f"{line}\n".encode())
                    time.sleep(0.1)  # Opóźnienie na wykonanie
            messagebox.showinfo("G-code", "G-code execution completed.")
        else:
            messagebox.showwarning("Warning", "No G-code content to run.")
