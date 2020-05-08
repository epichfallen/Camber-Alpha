from time import sleep
from umqtt.simple import MQTTClient


SERVER="10.3.141.1"
CLIENT_ID="ESP32"
TOPIC1=b"truewind/speed"
TOPIC2=b"truewind/angle"
TOPIC3=b"relativewind/speed"
TOPIC4=b"relativewind/angle"

def sub_cb(topic, msg):
	print((topic, msg))

client=MQTTClient(CLIENT_ID, SERVER)
client.connect()

while True:
	client.set_callback(sub_cb)
	client.subscribe(TOPIC1)
	
