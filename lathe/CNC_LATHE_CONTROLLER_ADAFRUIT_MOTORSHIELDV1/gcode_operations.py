import tkinter as tk
from tkinter import messagebox

class GCodeOperations:
    def __init__(self, app):
        self.app = app

    def add_operation_buttons(self, frame):
        threading_button = tk.Button(frame, text="Threading", command=self.configure_threading)
        threading_button.grid(row=0, column=0, padx=5, pady=5)

        grooving_button = tk.Button(frame, text="Grooving", command=self.configure_grooving)
        grooving_button.grid(row=0, column=1, padx=5, pady=5)

        drilling_button = tk.Button(frame, text="Drilling", command=self.configure_drilling)
        drilling_button.grid(row=1, column=0, padx=5, pady=5)

        rough_turning_button = tk.Button(frame, text="Rough Turning", command=self.configure_rough_turning)
        rough_turning_button.grid(row=1, column=1, padx=5, pady=5)

        finish_turning_button = tk.Button(frame, text="Finish Turning", command=self.configure_finish_turning)
        finish_turning_button.grid(row=1, column=2, padx=5, pady=5)

    def configure_threading(self):
        threading_window = tk.Toplevel(self.app.root)
        threading_window.title("Configure Threading")
        tk.Label(threading_window, text="Thread Length (mm):").pack()
        self.thread_length_var = tk.StringVar(value="20")
        tk.Entry(threading_window, textvariable=self.thread_length_var).pack()

        tk.Button(threading_window, text="Visualize Thread", command=self.visualize_threading).pack()
        tk.Button(threading_window, text="Start Threading", command=self.start_threading).pack()

    def visualize_threading(self):
        try:
            length = float(self.thread_length_var.get())
            self.app.ax.clear()
            self.app.ax.set_xlim(0, length + 10)
            self.app.ax.set_ylim(-10, 10)
            self.app.ax.grid(True)
            self.app.ax.set_xlabel("X Position (Thread Length)")
            self.app.ax.set_ylabel("Y Position")

            # Prosty model gwintu - cieńsza linia
            x_values = [0, length]
            y_values = [0, 0]
            self.app.ax.plot(x_values, y_values, 'g-', linewidth=0.5, label="Threading Path")
            self.app.ax.legend()
            self.app.canvas.draw()
        except ValueError:
            messagebox.showerror("Error", "Invalid thread length!")

    def start_threading(self):
        try:
            length = float(self.thread_length_var.get())
            command = f"G76 X10 Z{length} P1.5 Q0.3 R0.1"
            if self.app.serial_control.serial_port:
                self.app.serial_control.serial_port.write(f"{command}\n".encode())
            messagebox.showinfo("Threading", "Started threading.")
        except ValueError:
            messagebox.showerror("Error", "Invalid thread length!")

    def configure_grooving(self):
        grooving_window = tk.Toplevel(self.app.root)
        grooving_window.title("Configure Grooving")
        tk.Label(grooving_window, text="Groove Width (mm):").pack()
        self.groove_width_var = tk.StringVar(value="2")
        tk.Entry(grooving_window, textvariable=self.groove_width_var).pack()

        tk.Label(grooving_window, text="Groove Depth (mm):").pack()
        self.groove_depth_var = tk.StringVar(value="5")
        tk.Entry(grooving_window, textvariable=self.groove_depth_var).pack()

        tk.Label(grooving_window, text="Number of Grooves:").pack()
        self.groove_count_var = tk.StringVar(value="3")
        tk.Entry(grooving_window, textvariable=self.groove_count_var).pack()

        tk.Button(grooving_window, text="Visualize Grooving", command=self.visualize_grooving).pack()
        tk.Button(grooving_window, text="Start Grooving", command=self.start_grooving).pack()

    def visualize_grooving(self):
        try:
            width = float(self.groove_width_var.get())
            count = int(self.groove_count_var.get())
            self.app.ax.clear()
            self.app.ax.set_xlim(0, width * count + 10)
            self.app.ax.set_ylim(-10, 10)
            self.app.ax.grid(True)
            self.app.ax.set_xlabel("X Position")
            self.app.ax.set_ylabel("Y Position")

            # Rysowanie rowków - cieńsze linie
            for i in range(count):
                x_values = [width * i, width * i]
                y_values = [0, -5]
                self.app.ax.plot(x_values, y_values, 'b-', linewidth=0.5, label="Grooving" if i == 0 else "")
            self.app.ax.legend()
            self.app.canvas.draw()
        except ValueError:
            messagebox.showerror("Error", "Invalid groove parameters!")

    def start_grooving(self):
        try:
            width = float(self.groove_width_var.get())
            depth = float(self.groove_depth_var.get())
            count = int(self.groove_count_var.get())
            command = f"G75 X{width} Z{depth} P{count}"
            if self.app.serial_control.serial_port:
                self.app.serial_control.serial_port.write(f"{command}\n".encode())
            messagebox.showinfo("Grooving", "Started grooving.")
        except ValueError:
            messagebox.showerror("Error", "Invalid groove parameters!")

    def configure_drilling(self):
        drilling_window = tk.Toplevel(self.app.root)
        drilling_window.title("Configure Drilling")
        tk.Label(drilling_window, text="Drill Depth (mm):").pack()
        self.drill_depth_var = tk.StringVar(value="10")
        tk.Entry(drilling_window, textvariable=self.drill_depth_var).pack()

        tk.Label(drilling_window, text="Number of Peck Cycles:").pack()
        self.drill_pecks_var = tk.StringVar(value="5")
        tk.Entry(drilling_window, textvariable=self.drill_pecks_var).pack()

        tk.Button(drilling_window, text="Visualize Drilling", command=self.visualize_drilling).pack()
        tk.Button(drilling_window, text="Start Drilling", command=self.start_drilling).pack()

    def visualize_drilling(self):
        try:
            depth = float(self.drill_depth_var.get())
            self.app.ax.clear()
            self.app.ax.set_xlim(0, 10)
            self.app.ax.set_ylim(-depth - 5, 5)
            self.app.ax.grid(True)
            self.app.ax.set_xlabel("X Position")
            self.app.ax.set_ylabel("Depth Position")

            # Rysowanie ścieżki wiercenia - cieńsza linia
            x_values = [5, 5]
            y_values = [0, -depth]
            self.app.ax.plot(x_values, y_values, 'r-', linewidth=0.5, label="Drilling Path")
            self.app.ax.legend()
            self.app.canvas.draw()
        except ValueError:
            messagebox.showerror("Error", "Invalid drill depth!")

    def start_drilling(self):
        try:
            depth = float(self.drill_depth_var.get())
            pecks = int(self.drill_pecks_var.get())
            command = f"G74 Z{depth} P{pecks}"
            if self.app.serial_control.serial_port:
                self.app.serial_control.serial_port.write(f"{command}\n".encode())
            messagebox.showinfo("Drilling", "Started drilling.")
        except ValueError:
            messagebox.showerror("Error", "Invalid drill parameters!")

    def configure_rough_turning(self):
        rough_turning_window = tk.Toplevel(self.app.root)
        rough_turning_window.title("Configure Rough Turning")
        tk.Label(rough_turning_window, text="Diameter (mm):").pack()
        self.rough_diameter_var = tk.StringVar(value="50")
        tk.Entry(rough_turning_window, textvariable=self.rough_diameter_var).pack()

        tk.Label(rough_turning_window, text="Depth of Cut (mm):").pack()
        self.rough_cut_depth_var = tk.StringVar(value="5")
        tk.Entry(rough_turning_window, textvariable=self.rough_cut_depth_var).pack()

        tk.Label(rough_turning_window, text="Length (mm):").pack()
        self.rough_length_var = tk.StringVar(value="100")
        tk.Entry(rough_turning_window, textvariable=self.rough_length_var).pack()

        tk.Button(rough_turning_window, text="Visualize Rough Turning", command=self.visualize_rough_turning).pack()
        tk.Button(rough_turning_window, text="Start Rough Turning", command=self.start_rough_turning).pack()

    def visualize_rough_turning(self):
        try:
            diameter = float(self.rough_diameter_var.get())
            length = float(self.rough_length_var.get())
            self.app.ax.clear()
            self.app.ax.set_xlim(0, length + 10)
            self.app.ax.set_ylim(0, diameter + 10)
            self.app.ax.grid(True)
            self.app.ax.set_xlabel("Length Position")
            self.app.ax.set_ylabel("Diameter Position")

            x_values = [0, length]
            y_values = [diameter, diameter - 5]
            self.app.ax.plot(x_values, y_values, 'm-', linewidth=0.5, label="Rough Turning")
            self.app.ax.legend()
            self.app.canvas.draw()
        except ValueError:
            messagebox.showerror("Error", "Invalid rough turning parameters!")

    def start_rough_turning(self):
        try:
            diameter = float(self.rough_diameter_var.get())
            cut_depth = float(self.rough_cut_depth_var.get())
            length = float(self.rough_length_var.get())
            command = f"G71 X{diameter} Z{length} P{cut_depth}"
            if self.app.serial_control.serial_port:
                self.app.serial_control.serial_port.write(f"{command}\n".encode())
            messagebox.showinfo("Rough Turning", "Started rough turning.")
        except ValueError:
            messagebox.showerror("Error", "Invalid rough turning parameters!")

    def configure_finish_turning(self):
        finish_turning_window = tk.Toplevel(self.app.root)
        finish_turning_window.title("Configure Finish Turning")
        tk.Label(finish_turning_window, text="Diameter (mm):").pack()
        self.finish_diameter_var = tk.StringVar(value="48")
        tk.Entry(finish_turning_window, textvariable=self.finish_diameter_var).pack()

        tk.Label(finish_turning_window, text="Finish Length (mm):").pack()
        self.finish_length_var = tk.StringVar(value="100")
        tk.Entry(finish_turning_window, textvariable=self.finish_length_var).pack()

        tk.Button(finish_turning_window, text="Visualize Finish Turning", command=self.visualize_finish_turning).pack()
        tk.Button(finish_turning_window, text="Start Finish Turning", command=self.start_finish_turning).pack()

    def visualize_finish_turning(self):
        try:
            diameter = float(self.finish_diameter_var.get())
            length = float(self.finish_length_var.get())
            self.app.ax.clear()
            self.app.ax.set_xlim(0, length + 10)
            self.app.ax.set_ylim(0, diameter + 10)
            self.app.ax.grid(True)
            self.app.ax.set_xlabel("Length Position")
            self.app.ax.set_ylabel("Diameter Position")

            x_values = [0, length]
            y_values = [diameter, diameter]
            self.app.ax.plot(x_values, y_values, 'c-', linewidth=0.5, label="Finish Turning")
            self.app.ax.legend()
            self.app.canvas.draw()
        except ValueError:
            messagebox.showerror("Error", "Invalid finish turning parameters!")

    def start_finish_turning(self):
        try:
            diameter = float(self.finish_diameter_var.get())
            length = float(self.finish_length_var.get())
            command = f"G70 X{diameter} Z{length}"
            if self.app.serial_control.serial_port:
                self.app.serial_control.serial_port.write(f"{command}\n".encode())
            messagebox.showinfo("Finish Turning", "Started finish turning.")
        except ValueError:
            messagebox.showerror("Error", "Invalid finish turning parameters!")
