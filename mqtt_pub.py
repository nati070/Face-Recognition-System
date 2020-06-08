# MQTT Example.
# This example shows how to use the MQTT library to publish to a topic.
#
# 1) Copy the mqtt.py library to OpenMV storage.
# 2) Run this script on the OpenMV camera.
# 3) Install the mosquitto client on PC and run the following command:
#    mosquitto_sub -h test.mosquitto.org -t "openmv/test" -v
#
# NOTE: If the mosquitto broker is unreachable, try another broker (For example: broker.hivemq.com)
import time, network
from mqtt import MQTTClient

client = MQTTClient("openmv", "test.mosquitto.org", port=1883)
client.connect()

while (True):
    client.publish("openmv/test", "Hello World!")
    time.sleep(1000)
