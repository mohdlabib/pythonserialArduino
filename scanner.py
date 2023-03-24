import re
import pyautogui
import serial.tools.list_ports
import serial
import pystray
from PIL import Image

def get_serial_port():
    ports = serial.tools.list_ports.comports()
    portsList = []

    for onePort in ports:
        portsList.append(str(onePort))
        print(str(onePort))

    while True:
        val = input("Select Port: COM")
        for x in range(0,len(portsList)):
            if portsList[x].startswith("COM" + str(val)):
                portVar = "COM" + str(val)
                print(portVar)
                return portVar
        print("Port not found, please enter a valid port number.")

def on_quit(icon, item):
    icon.stop()
    serialInst.close()
    print("Application closed")

def main():
    portVar = get_serial_port()
    serialInst = serial.Serial(port=portVar, baudrate=9600)

    try:
        serialInst.open()
    except serial.SerialException as e:
        print(f"Error opening serial port {portVar}: {e}")
        return

    icon = pystray.Icon('Scanner')
    image = Image.open("icon.png")
    icon.menu = pystray.Menu(
        pystray.MenuItem(
            'Quit', 
            on_quit, 
            default=True,
        )
    )
    icon.icon = image
    icon.title = 'Scanner'
    icon.run(setup=icon.visible)

    while True:
        data = serialInst.readline().decode().rstrip()
        match = re.match("^[0-9]*$", data)
        if match:
            pyautogui.write(data)

if __name__ == '__main__':
    main()
