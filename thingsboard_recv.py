import os
import paho.mqtt.client as mqtt
#import RPi.GPIO as GPIO
import json
from dotenv import load_dotenv
from pyplantApp import ArduinoBoard
import time

load_dotenv()

THINGSBOARD_HOST = os.environ['THINGSBOARD_HOST']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
INTERVAL=2

sensor_data = {
    'temperature': 0, 
    'humidity': 0,
    'distance': 0,
    'light_value': 0,
    'water_level': 0,
    'soil_moisture': 0,
    }

arduino = ArduinoBoard()

"""
# We assume that all GPIOs are LOW
gpio_state = {7: False, 11: False, 12: False, 13: False, 15: False, 16: False, 18: False, 22: False, 29: False,
              31: False, 32: False, 33: False, 35: False, 36: False, 37: False, 38: False, 40: False}
"""

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    # print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')
    # Sending current GPIO status
    # client.publish('v1/devices/me/attributes', get_gpio_status(), 1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print 'Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload)
    # Decode JSON request
    data = json.loads(msg.payload)
    # Check request method
    print(data)
    if data["method"] == "run_water_pump":
        time.sleep(1)
        arduino.run_water_pump()
        time.sleep(arduino.run_water_pump_time+1) # wait for the pump to stop running
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
    
    """
    elif data['method'] == 'setGpioStatus':
        # Update GPIO status and reply
        set_gpio_status(data['params']['pin'], data['params']['enabled'])
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        client.publish('v1/devices/me/attributes', get_gpio_status(), 1)
    """

"""
def get_gpio_status():
    # Encode GPIOs state to json
    return json.dumps(gpio_state)


def set_gpio_status(pin, status):
    # Output GPIOs state
    GPIO.output(pin, GPIO.HIGH if status else GPIO.LOW)
    # Update GPIOs state
    gpio_state[pin] = status


# Using board GPIO layout
GPIO.setmode(GPIO.BOARD)
for pin in gpio_state:
    # Set output mode for all GPIO pins
    GPIO.setup(pin, GPIO.OUT)
"""


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

    next_reading = time.time() 

    try:
        client.loop_start()
        while True:
            arduino.read_sensors()           

            sensor_data['temperature'] = arduino.temperature
            sensor_data['humidity'] = arduino.humidity
            sensor_data['distance'] = arduino.distance
            sensor_data['light_value'] = arduino.light_value
            sensor_data['water_level'] = arduino.water_level
            sensor_data['soil_moisture'] = arduino.soil_moisture
            print(arduino.soil_moisture)
            print("Temperature: {}, Humidity: {}%".format(sensor_data["temperature"], sensor_data["humidity"]))
            # Sending humidity and temperature data to ThingsBoard
            client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
            next_reading += INTERVAL
            sleep_time = next_reading-time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)

            if(arduino.automate_watering == True):
                arduino.auto_watering() 
    except KeyboardInterrupt:
        pass

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()