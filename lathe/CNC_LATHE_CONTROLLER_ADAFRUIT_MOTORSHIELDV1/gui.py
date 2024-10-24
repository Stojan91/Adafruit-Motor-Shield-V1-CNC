import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gcode_operations import GCodeOperations
from serial_control import SerialControl
from gcode_runner import GCodeRunner

class CNCLatheControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CNC Lathe Controller")
        self.serial_control = SerialControl()
        self.gcode_operations = GCodeOperations(self)
        self.gcode_runner = GCodeRunner(self)
        self.x_position = 0
        self.y_position = 0

        # Konfiguracja GUI
        self.create_widgets()

    def create_widgets(self):
        # Ramka do elementów kontrolnych po lewej stronie
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        # Sekcja wyboru portu
        self.port_label = tk.Label(control_frame, text="Select Port:")
        self.port_label.grid(row=0, column=0, padx=5, pady=5)

        # Pobierz listę portów i ustaw wartość domyślną
        ports = self.serial_control.get_serial_ports()
        if ports:
            self.port_var = tk.StringVar(value=ports[0])
        else:
            self.port_var = tk.StringVar(value="No Ports Available")
            ports = ["No Ports Available"]
        
        self.port_menu = tk.OptionMenu(control_frame, self.port_var, *ports)
        self.port_menu.grid(row=0, column=1, padx=5, pady=5)

        self.refresh_button = tk.Button(control_frame, text="Refresh Ports", command=self.refresh_ports)
        self.refresh_button.grid(row=0, column=2, padx=5, pady=5)

        # Menu rozwijane do wyboru baudrate
        self.baud_label = tk.Label(control_frame, text="Baudrate:")
        self.baud_label.grid(row=1, column=0, padx=5, pady=5)
        self.baud_options = [9600, 19200, 38400, 57600, 115200]
        self.baud_var = tk.StringVar(value=self.baud_options[0])
        self.baud_menu = tk.OptionMenu(control_frame, self.baud_var, *self.baud_options)
        self.baud_menu.grid(row=1, column=1, padx=5, pady=5)

        self.connect_button = tk.Button(control_frame, text="Connect", command=self.connect_to_port)
        self.connect_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Przycisk bezpieczeństwa STOP
        self.stop_button = tk.Button(control_frame, text="STOP", command=self.serial_control.emergency_stop, bg="red", fg="white")
        self.stop_button.grid(row=2, column=2, padx=5, pady=5)

        # Sekcja sterowania ręcznego
        self.manual_frame = tk.LabelFrame(control_frame, text="Manual Control")
        self.manual_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.up_button = tk.Button(self.manual_frame, text="Up", width=10, command=lambda: self.send_manual_command("UP"))
        self.up_button.grid(row=0, column=1)

        self.left_button = tk.Button(self.manual_frame, text="Left", width=10, command=lambda: self.send_manual_command("LEFT"))
        self.left_button.grid(row=1, column=0)

        self.right_button = tk.Button(self.manual_frame, text="Right", width=10, command=lambda: self.send_manual_command("RIGHT"))
        self.right_button.grid(row=1, column=2)

        self.down_button = tk.Button(self.manual_frame, text="Down", width=10, command=lambda: self.send_manual_command("DOWN"))
        self.down_button.grid(row=2, column=1)

        # Sekcja zaawansowanych cykli obróbczych
        self.advanced_frame = tk.LabelFrame(control_frame, text="Advanced Operations")
        self.advanced_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.gcode_operations.add_operation_buttons(self.advanced_frame)

        # Sekcja wysyłania pliku G-code z podglądem
        self.upload_button = tk.Button(control_frame, text="Upload G-code", command=self.gcode_runner.preview_gcode)
        self.upload_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # Dodanie logo pod przyciskiem "Upload G-code"
        try:
            self.logo_image = Image.open("data/logo.gif")
            self.logo_image = self.logo_image.resize((200, 110), Image.ANTIALIAS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(control_frame, image=self.logo_photo)
            self.logo_label.grid(row=6, column=0, columnspan=3, pady=10)
        except Exception as e:
            print(f"Error loading logo: {e}")

        # Sekcja wizualizacji z siatką i osiami po prawej stronie
        self.figure, self.ax = plt.subplots()
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(-100, 100)
        self.ax.grid(True)  # Dodanie siatki
        self.ax.set_xlabel("X Position")
        self.ax.set_ylabel("Y Position")
        self.position_dot, = self.ax.plot(self.x_position, self.y_position, 'bo')

        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=7, padx=10, pady=10, sticky="ns")

    def refresh_ports(self):
        # Odśwież listę portów
        ports = self.serial_control.get_serial_ports()
        if ports:
            self.port_var.set(ports[0])
        else:
            self.port_var.set("No Ports Available")
            ports = ["No Ports Available"]

        self.port_menu['menu'].delete(0, 'end')
        for port in ports:
            self.port_menu['menu'].add_command(label=port, command=tk._setit(self.port_var, port))

    def connect_to_port(self):
        port_name = self.port_var.get()
        baudrate = int(self.baud_var.get())
        self.serial_control.connect_to_port(port_name, baudrate)

    def send_manual_command(self, direction):
        # Wyślij komendę ręczną do tokarki
        if not self.serial_control.serial_port:
            messagebox.showerror("Error", "Not connected to any port")
            return

        command = ""
        if direction == "UP":
            command = "G1 Y1"
            self.y_position += 1
        elif direction == "DOWN":
            command = "G1 Y-1"
            self.y_position -= 1
        elif direction == "LEFT":
            command = "G1 X-1"
            self.x_position -= 1
        elif direction == "RIGHT":
            command = "G1 X1"
            self.x_position += 1

        # Aktualizacja wizualizacji pozycji
        self.update_visualization()
        self.serial_control.serial_port.write((command + "\n").encode())

    def update_visualization(self):
        # Aktualizacja pozycji punktu na wykresie
        self.position_dot.set_data(self.x_position, self.y_position)
        self.ax.set_xlim(min(self.x_position - 10, -100), max(self.x_position + 10, 100))
        self.ax.set_ylim(min(self.y_position - 10, -100), max(self.y_position + 10, 100))
        self.canvas.draw()
