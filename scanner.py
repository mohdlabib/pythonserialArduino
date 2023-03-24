import re
import pyautogui
import serial.tools.list_ports
import serial

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: COM")

for x in range(0,len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)

serialInst.baudrate = 9600
serialInst.port = portVar

try:
    serialInst.close()
except:
    pass

serialInst.open()

while True:
    data = serialInst.readline().decode().rstrip()
    match = re.match("^[0-9]*$", data)
    if match:
        pyautogui.write(data)