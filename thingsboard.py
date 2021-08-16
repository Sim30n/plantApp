import os
import time
import sys
import paho.mqtt.client as mqtt
import json
from pyplantApp import ArduinoBoard
from dotenv import load_dotenv

load_dotenv()

THINGSBOARD_HOST = os.environ['THINGSBOARD_HOST']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=10

sensor_data = {'temperature': 0, 'humidity': 0}

arduino = ArduinoBoard()

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()



try:
    while True:
        #humidity,temperature = dht.read_retry(dht.DHT22, 4)
        arduino.read_sensors()
        humidity = arduino.humidity
        temperature = arduino.temperature
        print(u"Temperature: {}, Humidity: {}%".format(temperature, humidity))
        sensor_data['temperature'] = temperature
        sensor_data['humidity'] = humidity

        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()