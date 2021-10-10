import unittest
from pyplantApp import ArduinoBoard
from datetime import datetime

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.arduino_board = ArduinoBoard()
        self.arduino_board.time_stamp = None
        self.arduino_board.distance = None # remove when not used!
        self.arduino_board.humidity = None
        self.arduino_board.temperature = None
        self.arduino_board.light_value = None
        self.arduino_board.water_level = None
        self.arduino_board.soil_moisture = None
        self.arduino_board.run_water_pump_time = None
        self.arduino_board.automate_watering = False
        self.arduino_board.min_soil_moisture = 0
        self.arduino_board.last_pump_run = datetime.now()
        self.arduino_board.water_tank_volume = None
    
    def tearDown(self):
        #self.arduino_board.close_serial()
        pass
    
    def test_water_pump(self):
        self.arduino_board.run_water_pump_time = 10
        pump_run = self.arduino_board.run_water_pump()
        self.assertEqual(pump_run, "Water pump ran for 10 seconds.")

    def test_calculate_container_volume(self):
        tank_volume = self.arduino_board.calculate_water_tank_volume(20)
        self.assertEqual(tank_volume, 16.45)


if __name__ == "__main__":
    unittest.main()