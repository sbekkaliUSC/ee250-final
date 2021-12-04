""" EE 250 Final Project
Team members: Saleem Bekkali
Repo: https://github.com/sbekkaliUSC/ee250-final
"""

import sys
import time
import paho.mqtt.client as mqtt
import grovepi
from grovepi import *

threshold = 50 # default value
def custom_callback_threshold(client, userdata, message):
    msg = message.payload.decode('utf-8', 'strict')
    threshold = int(msg)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("bekkali/threshold")
    client.message_callback_add("bekkali/threshold", custom_callback_threshold)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':

    led = 3 # D3
    ultrasonic = 4    # D4
    pinMode(led,"OUTPUT")

    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        try:
            #sleep 1 second
            time.sleep(1)

            distance = grovepi.ultrasonicRead(ultrasonic) # measures distance via ultrasonic sensor
            if (distance <= threshold):
                client.publish("bekkali/ultrasonicRanger", 1)
                digitalWrite(led, 1)
            else:
                client.publish("bekkali/ultrasonicRanger", 0)
                digitalWrite(led, 0)
        except KeyboardInterrupt:
            digitalWrite(led, 0)

        except (IOError,TypeError) as e:
            print(e)
