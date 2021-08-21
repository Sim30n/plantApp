# pyplantApp.py

import serial
import time
from datetime import datetime, timedelta

class ArduinoBoard:
    ser = serial.Serial("/dev/ttyACM0", 9600)
    time.sleep(2)

    def __init__(self):
        self.time_stamp = None
        self.distance = None
        self.humidity = None
        self.temperature = None
        self.light_value = None
        self.water_level = None
        self.soil_moisture = None
        self.run_water_pump_time = 0 # set time from thingsboard
        self.automate_watering = False
        self.min_soil_moisture = 1000
        self.last_pump_run = datetime.now()

    def read_sensors(self):
        self.ser.write(str.encode("read_sensors"))
        time.sleep(3)
        result = self.ser.readline().decode("utf-8")
        strip_result = result.strip()
        split_result = strip_result.split(";")
        self.distance = split_result[0]
        self.humidity = split_result[1]
        self.temperature = split_result[2]
        self.light_value = split_result[3]
        self.water_level = split_result[4]
        self.soil_moisture = int(split_result[5])
        self.time_stamp = datetime.now()
        time.sleep(1)
        
    def run_water_pump(self):
        if(self.run_water_pump_time != 0):
            run_command = "run_water_pump" + str(self.run_water_pump_time)
            print(run_command)
            self.ser.write(str.encode(run_command))
            self.last_pump_run = datetime.now()
            #time.sleep(self.run_water_pump_time+1)
            
    """
    def auto_watering(self):
        time_now = datetime.now()
        time_difference = time_now - self.last_pump_run
        minutes  = timedelta(seconds=60)
        print(time_difference.total_seconds())
        if(self.soil_moisture < self.min_soil_moisture and time_difference > minutes):
            self.run_water_pump()
    """
    def switch_light(self, position):
        pass
    
    def save_sensor_values(self):
        pass

    def close_serial(self):
        self.ser.close()
