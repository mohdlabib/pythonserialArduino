import re
import pyautogui
import serial.tools.list_ports
from colorama import init, Fore, Style

init(autoreset=True)

# Get list of available ports
ports = serial.tools.list_ports.comports()
portsList = [str(port) for port in ports]

# Print out available ports in yellow
print(Fore.YELLOW + "Available Ports:")
for port in portsList:
    print(port)

# Ask the user to select a port
while True:
    try:
        val = input(Style.BRIGHT + Fore.BLUE + "Select Port: COM")
        if not re.match("^[0-9]+$", val):
            raise ValueError
        val = int(val)
        portVar = "COM" + str(val)
        if not any(portVar in port for port in portsList):
            raise ValueError
        break
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a valid COM port number.")

# Set the selected port as the serial instance's port
serialInst = serial.Serial(port=portVar, baudrate=9600)
serialInst.open()

# Main loop to read data from serial port and write to command prompt
while True:
    data = serialInst.readline().decode().rstrip()
    match = re.match("^[0-9]*$", data)
    if match:
        pyautogui.write(data)
