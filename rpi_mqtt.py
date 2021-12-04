""" EE 250 Final Project
Team members: Saleem Bekkali
Repo: https://github.com/sbekkaliUSC/ee250-final
Source: Reusing parts of code from grovepi_sensors.py and rpi_pub_and_sub.py
from Lab 2 and 5, respectively.
"""

"""python3 interpreters in Ubuntu (and other linux distros) will look in a 
default set of directories for modules when a program tries to `import` one. 
Examples of some default directories are (but not limited to):
  /usr/lib/python3.5
  /usr/local/lib/python3.5/dist-packages

The `sys` module, however, is a builtin that is written in and compiled in C for
performance. Because of this, you will not find this in the default directories.
"""
import sys
import time
import paho.mqtt.client as mqtt

# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

import grovepi
from grove_rgb_lcd import *

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    """#subscribe to topics of interest here
    client.subscribe("bekkali/led")
    client.message_callback_add("bekkali/led", custom_callback_led)

    client.subscribe("bekkali/lcd")
    client.message_callback_add("bekkali/lcd", custom_callback_lcd)"""

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':

    led = 3 # D3
    ultrasonic = 4    # D4

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
            threshold = 50 # TEMPORARY TEST VALUE

            if (distance <= threshold):
                #client.publish("bekkali/ultrasonicRanger", 1)
                digitalWrite(led, 1)
            else:
                #client.publish("bekkali/ultrasonicRanger", 0)
                digitalWrite(led, 0)


        except (IOError,TypeError) as e:
            print("Error")
