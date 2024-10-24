import serial
import serial.tools.list_ports
from tkinter import messagebox

class SerialControl:
    def __init__(self):
        self.serial_port = None

    def get_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect_to_port(self, port_name, baudrate):
        try:
            self.serial_port = serial.Serial(port_name, baudrate, timeout=1)
            messagebox.showinfo("Connection", f"Connected to {port_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")

    def emergency_stop(self):
        if self.serial_port:
            self.serial_port.write("M112\n".encode())  # Typowy kod zatrzymania w G-code
            self.serial_port.close()
            messagebox.showinfo("Emergency Stop", "Emergency stop activated!")
