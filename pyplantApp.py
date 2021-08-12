# pyplantApp.py

import serial
import time

class ArduinoBoard:
    ser = serial.Serial("/dev/ttyACM0", 9600)
    time.sleep(2)

    def __init__(self):
        self.humidity = ""

    def read_sensors(self):
        self.ser.write(str.encode("read_sensors"))
        time.sleep(3)
        result = self.ser.readline().decode("utf-8")
        print(result)
        #ser.close()

arduino = ArduinoBoard()

arduino.read_sensors()