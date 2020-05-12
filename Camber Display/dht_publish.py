from time import sleep
from umqtt.simple import MQTTClient
import network
import ubinascii


unique_id=ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
statetopic= "display/espdisplay:"+str(unique_id)+"/state"

SERVER="10.3.141.1"
CLIENT_ID= "ESP DISPLAY: " + str(unique_id)

TOPIC1=b"truewind/speed"
TOPIC2=b"truewind/angle"
TOPIC3=b"relativewind/speed"
TOPIC4=b"relativewind/angle"

def sub_cb(topic, msg):
	print((topic, msg))

client=MQTTClient(CLIENT_ID, SERVER,keepalive=2)

client.set_last_will(statetopic,"Offline",retain=True,qos=0)
client.connect()

client.publish(statetopic,'Online',retain=True,qos=0)

while True:
	client.set_callback(sub_cb)
	client.subscribe(TOPIC1)
	
