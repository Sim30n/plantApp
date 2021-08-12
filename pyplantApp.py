# pyplantApp.py

import serial
import time

class ArduinoBoard:
    ser = serial.Serial("/dev/ttyACM0", 9600)
    time.sleep(2)

    def __init__(self):
        self.humidity = 0
        self.temperature = 0
        self.water_level = 0
        self.soil_moisture = 0
        self.water_tank_level = 0

    def read_sensors(self):
        self.ser.write(str.encode("read_sensors"))
        time.sleep(3)
        result = self.ser.readline().decode("utf-8")
        print(result)
        #ser.close()
        
    def run_water_pump(self, pump, position):
        pass
    
    def switch_light(self, position):
        pass
    
    def save_sensor_values(self):
        pass
    
arduino = ArduinoBoard()

arduino.read_sensors()
