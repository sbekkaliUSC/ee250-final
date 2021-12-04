""" EE 250 Final Project
Team members: Saleem Bekkali
Repo: https://github.com/sbekkaliUSC/ee250-final
"""

import sys
import paho.mqtt.client as mqtt
import time
from collections import deque
import threading
lock = threading.Lock()

def custom_callback_UR(client, userdata, message):
    msg = message.payload.decode('utf-8', 'strict')
    print(msg)
    with lock:
        if len(queue) == 60:
            queue.popleft() # removes oldest boolean in queue to free up space
        queue.append(msg == "1") # if within UR range put True else put False

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("bekkali/ultrasonicRanger")
    client.message_callback_add("bekkali/ultrasonicRanger", custom_callback_UR)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def compute_objects_minute(queue):
    total_detected = 0
    object_present = False
    for i in queue:
        if not object_present and i: # true if object first detected
            total_detected += 1
        object_present = i
    return total_detected


if __name__ == '__main__':
    try:
        if (len(sys.argv) >= 2):
            threshold = int(sys.argv[1])
            if threshold < 0 or threshold > 517:
                print("Warning: Threshold values outside of range [0, 517] are unreliable")
        queue = deque([])
        client = mqtt.Client()
        client.on_message = on_message
        client.on_connect = on_connect
        client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
        client.loop_start()
        if (len(sys.argv) >= 2):
            client.publish("bekkali/threshold", threshold)

        while True:
            time.sleep(10)
            with lock:
                print("Objects detected:%d", compute_objects_minute(queue))
                print(queue)
    except ValueError:
        print("Specified Threshold value must be an integer formatted as \"/python3 vm_mqtt.py [threshold]\".")

            

