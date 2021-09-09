import os
import paho.mqtt.client as mqtt
import json
from dotenv import load_dotenv
from pyplantApp import ArduinoBoard
import time
from datetime import datetime, timedelta

load_dotenv()

THINGSBOARD_HOST = os.environ['THINGSBOARD_HOST']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
INTERVAL=2

sensor_data = {
    "temperature": 0, 
    "humidity": 0,
    "distance": 0,
    "light_value": 0,
    "water_level": 0,
    "soil_moisture": 0,
    "tank_volume":0,
    }

arduino = ArduinoBoard()

def on_connect(client, userdata, rc, *extra_params):
    """
    The callback for when the client receives a CONNACK response from the server.
    """
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')

def on_message(client, userdata, msg):
    """
    The callback for when a PUBLISH message is received from the server.
    """
    # Decode JSON request
    data = json.loads(msg.payload)
    # Check request method
    print(data) # prints the incoming message from thingsboard
    if data["method"] == "run_water_pump":
        run_pumps()

    elif data['method'] == 'getPumpRuntime':
        # Reply getPumpRuntime 
        client.publish(msg.topic.replace('request', 'response'), arduino.run_water_pump_time, 1)
    elif data['method'] == 'setPumpRuntime':
        # set pump run time
        arduino.run_water_pump_time = data["params"]
    elif data['method'] == 'setAutoWatering':
        arduino.automate_watering = data["params"]
    elif data['method'] == 'getAutoWatering':    
        client.publish(msg.topic.replace('request', 'response'), int(arduino.automate_watering), 1)

    elif data['method'] == 'getFertilizer1':
        # Reply getPumpRuntime 
        client.publish(msg.topic.replace('request', 'response'), arduino.fertilizer_1_pump_time, 1)
    elif data['method'] == 'setFertilizer1':
        # set pump run time
        arduino.fertilizer_1_pump_time = data["params"]

    elif data['method'] == 'getFertilizer2':
        # Reply getPumpRuntime 
        client.publish(msg.topic.replace('request', 'response'), arduino.fertilizer_2_pump_time, 1)
    elif data['method'] == 'setFertilizer2':
        # set pump run time
        arduino.fertilizer_2_pump_time = data["params"]
    
    elif data['method'] == 'getFertilizer3':
        # Reply getPumpRuntime 
        client.publish(msg.topic.replace('request', 'response'), arduino.fertilizer_3_pump_time, 1)
    elif data['method'] == 'setFertilizer3':
        # set pump run time
        arduino.fertilizer_3_pump_time = data["params"]
    
    elif data['method'] == 'getFertilizer4':
        # Reply getPumpRuntime 
        client.publish(msg.topic.replace('request', 'response'), arduino.fertilizer_4_pump_time, 1)
    elif data['method'] == 'setFertilizer4':
        # set pump run time
        arduino.fertilizer_4_pump_time = data["params"]

    elif data['method'] == 'getSoilMoisture':
        # Reply getPumpRuntime 
        client.publish(msg.topic.replace('request', 'response'), arduino.min_soil_moisture, 1)
    elif data['method'] == 'setSoilMoisture':
        # set pump run time
        arduino.min_soil_moisture = data["params"]

def run_pumps():
    """
    Function for running the water pump and fertilizer pumps.
    """
    time.sleep(1)
    arduino.run_fertilizer_pump("07", str(arduino.fertilizer_1_pump_time))
    time.sleep(arduino.fertilizer_1_pump_time+2)

    arduino.run_fertilizer_pump("11", str(arduino.fertilizer_2_pump_time))
    time.sleep(arduino.fertilizer_2_pump_time+2)

    arduino.run_fertilizer_pump("12", str(arduino.fertilizer_3_pump_time))
    time.sleep(arduino.fertilizer_3_pump_time+2)

    arduino.run_fertilizer_pump("13", str(arduino.fertilizer_4_pump_time))
    time.sleep(arduino.fertilizer_4_pump_time+2)
    
    arduino.run_water_pump()
    time.sleep(arduino.run_water_pump_time+2) # wait for the pump to stop running

def main():
    client = mqtt.Client()
    # Register connect callback
    client.on_connect = on_connect
    # Registed publish message callback
    client.on_message = on_message
    # Set access token
    client.username_pw_set(ACCESS_TOKEN)
    # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
    client.connect(THINGSBOARD_HOST, 1883, 60)
    # time for interval logic
    next_reading = time.time() 

    try:
        client.loop_start()
        while True:
            
            # Read the sensors, print values to the terminal
            # and puplish values as telemetry data to thing board
            
            arduino.read_sensors()           
            sensor_data['temperature'] = arduino.temperature
            sensor_data['humidity'] = arduino.humidity
            sensor_data['distance'] = arduino.distance
            sensor_data['light_value'] = arduino.light_value
            sensor_data['water_level'] = arduino.water_level
            sensor_data['soil_moisture'] = arduino.soil_moisture
            sensor_data["tank_volume"] = arduino.water_tank_volume
            print("temperature:{}, " 
                  "humidity:{}%, "
                  "(water tank)distance:{}, "
                  "light:{}, " 
                  "water_level:{}, " 
                  "soil_moisture:{}, "
                  "tank_volume:{}"
                  .format(sensor_data["temperature"],
                          sensor_data["humidity"], 
                          sensor_data['distance'], 
                          sensor_data['light_value'],
                          sensor_data['water_level'],
                          sensor_data['soil_moisture'],
                          sensor_data['tank_volume']))
            client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        
            # This logic is for determining the time difference between sending 
            # the arduino sensor data to the Thingsboard user interface.
            
            next_reading += INTERVAL
            sleep_time = next_reading-time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    
            # This logic is for using the water automation option.
              
            time_now = datetime.now()
            time_difference = time_now - arduino.last_pump_run
            minutes = timedelta(seconds=60)   
            if arduino.automate_watering == True and  \
               arduino.soil_moisture < arduino.min_soil_moisture and \
               time_difference > minutes:
                run_pumps()
                #arduino.run_water_pump() 
                #time.sleep(arduino.run_water_pump_time+1)

    except KeyboardInterrupt:
        arduino.close_serial()
        pass

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()