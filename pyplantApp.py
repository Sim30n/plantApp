# pyplantApp.py

import serial
import time
from datetime import datetime, timedelta

class ArduinoBoard:
    ser = serial.Serial("/dev/ttyACM0", 9600)
    time.sleep(2)

    def __init__(self):
        self.time_stamp = None
        self.distance = None # remove when not used!
        self.humidity = None
        self.temperature = None
        self.light_value = None
        self.water_level = None
        self.soil_moisture = None
        self.run_water_pump_time = 0 # set time from thingsboard
        self.automate_watering = False
        self.min_soil_moisture = 0
        self.last_pump_run = datetime.now()
        self.water_tank_volume = None
        self.read_sensors()
        #self.calculate_water_tank_volume()

        self.fertilizer_1_pump_time = 0
        self.fertilizer_2_pump_time = 0
        self.fertilizer_3_pump_time = 0
        self.fertilizer_4_pump_time = 0

    def read_sensors(self):
        self.ser.write(str.encode("read_sensors"))
        time.sleep(3)
        result = self.ser.readline().decode("utf-8")
        strip_result = result.strip()
        split_result = strip_result.split(";")
        self.distance = int(split_result[0])
        self.humidity = split_result[1]
        self.temperature = split_result[2]
        self.light_value = split_result[3]
        self.water_level = split_result[4]
        self.soil_moisture = int(split_result[5])
        self.time_stamp = datetime.now()
        self.water_tank_volume = self.calculate_water_tank_volume(int(split_result[0]))
        time.sleep(1)
        
    def run_water_pump(self):
        if(self.run_water_pump_time != 0):
            run_command = "run_water_pump" + str(self.run_water_pump_time)
            #print(run_command)
            self.ser.write(str.encode(run_command))
            self.last_pump_run = datetime.now()
            #time.sleep(self.run_water_pump_time+1)

    def calculate_water_tank_volume(self, distance):
        height = 45
        width = 23.5
        depth = 28
        water_tank_volume = (((height - distance) 
                               * width * depth) / 1000) # liters
        return water_tank_volume

    def run_fertilizer_pump(self, pump_n, run_time):
        """Return None

        Method for running fertilizer pump.
        TODO: Resolve how to determine pump numbeer and run time.            
        """
        #pump_n = "07"
        #run_fertilizer_pump_time = 100
        print(pump_n, run_time)
        if(int(run_time) != 0):
            run_command = ("run_fertilizer_pump" 
                        + pump_n 
                        + run_time)
            self.ser.write(str.encode(run_command))
        
    def switch_light(self, position):
        pass
    
    def save_sensor_values(self):
        pass

    def close_serial(self):
        self.ser.close()
