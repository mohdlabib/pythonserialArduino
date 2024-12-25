import re
import pyautogui
import serial.tools.list_ports
import serial
import tkinter as tk
from tkinter import messagebox, ttk
from playsound import playsound
import os
import threading
import time

connected_ports = set()
serial_inst = None


def list_ports():
    """Menampilkan daftar port yang terdeteksi."""
    ports = serial.tools.list_ports.comports()
    return [str(port) for port in ports]


def connect_to_serial(port, baudrate=9600):
    """Menghubungkan ke port serial."""
    serial_inst = serial.Serial()
    serial_inst.baudrate = baudrate
    serial_inst.port = port

    try:
        serial_inst.close()
    except:
        pass

    try:
        serial_inst.open()
        return serial_inst
    except Exception as e:
        messagebox.showerror("Error", f"Could not open port {port}.\n{e}")
        return None


def start_reading(serial_inst):
    """Membaca data secara terus-menerus dari serial port."""
    while True:
        try:
            raw_data = serial_inst.readline()
            data = raw_data.decode('utf-8', errors='ignore').rstrip()
            print(f"Decoded data: {data}")

            if re.match(r"^[A-F0-9]+$", data.upper()):
                sound_path = os.path.join(os.getcwd(), 'sound.mp3')
                if os.path.exists(sound_path):
                    playsound(sound_path)
                else:
                    print("Sound file not found.")
                pyautogui.write(data)
            else:
                print(f"Ignored data: {data}")
        except Exception as e:
            messagebox.showerror("Error", f"Error reading data: {e}")
            break


def on_connect():
    """Menangani koneksi saat tombol Connect diklik."""
    selected_port = combo_ports.get()
    if not selected_port:
        messagebox.showwarning("Warning", "Please select a COM port.")
        return

    if selected_port in connected_ports:
        messagebox.showinfo("Info", f"Already connected to {selected_port}")
        return

    global serial_inst
    serial_inst = connect_to_serial(selected_port.split()[0])
    if serial_inst:
        connected_ports.add(selected_port)
        root.after(0, update_status, f"Connected to {selected_port}", "green")
        threading.Thread(target=start_reading, args=(serial_inst,), daemon=True).start()


def update_ports():
    """Memperbarui daftar port serial yang tersedia."""
    available_ports = [port for port in list_ports() if port not in connected_ports]
    if set(combo_ports['values']) != set(available_ports):
        combo_ports['values'] = available_ports


def detect_new_ports():
    """Mendeteksi port baru yang terhubung secara real-time."""
    global connected_ports
    while True:
        current_ports = set(list_ports())
        if current_ports != connected_ports:
            root.after(0, update_ports)
        time.sleep(2)


def update_status(message, color):
    """Mengupdate label status."""
    label_status.config(text=message, foreground=color)


# GUI dengan Tkinter
root = tk.Tk()
root.title("Arduino Serial Reader")

icon_path = os.path.join(os.getcwd(), "icon.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Select COM Port:").grid(row=0, column=0, pady=5)
combo_ports = ttk.Combobox(frame, values=list_ports(), state="readonly")
combo_ports.grid(row=0, column=1, pady=5)

btn_connect = ttk.Button(frame, text="Connect", command=on_connect)
btn_connect.grid(row=1, column=0, columnspan=2, pady=10)

label_status = ttk.Label(frame, text="Status: Disconnected", foreground="red")
label_status.grid(row=2, column=0, columnspan=2, pady=10)

btn_refresh = ttk.Button(frame, text="Refresh Ports", command=update_ports)
btn_refresh.grid(row=3, column=0, columnspan=2, pady=5)

thread = threading.Thread(target=detect_new_ports, daemon=True)
thread.start()

root.mainloop()
