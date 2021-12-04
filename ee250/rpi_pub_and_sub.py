#Team members: Saleem Bekkali
#Repo: https://github.com/usc-ee250-fall2021/lab05-saleem5

"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import grovepi
from grovepi import *
from grove_rgb_lcd import *
import threading
lock = threading.Lock()

def custom_callback_led(client, userdata, message):
    msg = message.payload.decode('utf-8', 'strict')
    if (msg == "LED_ON"):
        #print("LED is on")
        with lock:
            digitalWrite(led, 1)
    if (msg == "LED_OFF"):
        #print("LED is off")
        with lock:
            digitalWrite(led, 0)


def custom_callback_lcd(client, userdata, message):
    msg = message.payload.decode('utf-8', 'strict')
    try:
        with lock:
            setText_norefresh(msg)
    except IOError:
            print("IOError")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("bekkali/led")
    client.message_callback_add("bekkali/led", custom_callback_led)

    client.subscribe("bekkali/lcd")
    client.message_callback_add("bekkali/lcd", custom_callback_lcd)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    led = 4 # digital port D4
    button = 3 # digital port D3
    UR = 2 # digital port D2
    pinMode(led,"OUTPUT")
    pinMode(button, "INPUT")
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        try:
            time.sleep(1)
            with lock:
                button_status = digitalRead(button)
            with lock:
                UR_input = ultrasonicRead(UR)
            if button_status: # if button is pressed
                client.publish("bekkali/button", "Button pressed!")
            client.publish("bekkali/ultrasonicRanger", UR_input)
        except KeyboardInterrupt:
            with lock: 
                digitalWrite(led, 0)
        except IOError:
            print("IOError")

