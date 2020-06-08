import time, network, pyb
from mqtt import MQTTClient
SSID='HOTBOX-3E602'
KEY='0542051321'
def sub_cb(topic, msg):
	print((topic, msg))
print("Trying to connect... (may take a while)...")
wlan = network.WINC()
wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)
print(wlan.ifconfig())
client = MQTTClient("openmv", "test.mosquitto.org", port=1883)
client.set_callback(sub_cb)
client.connect()
client.subscribe("openmv/test")
while True:
	client.wait_msg()