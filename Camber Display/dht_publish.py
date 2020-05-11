from time import sleep
from umqtt.simple import MQTTClient
import machine

unique_id=machine.unique_id()
statetopic= "display/"+unique_id+"/state"



SERVER="10.3.141.1"
CLIENT_ID= "ESP DISPLAY: " + unique_id 


TOPIC1=b"truewind/speed"
TOPIC2=b"truewind/angle"
TOPIC3=b"relativewind/speed"
TOPIC4=b"relativewind/angle"

def sub_cb(topic, msg):
	print((topic, msg))

client=MQTTClient(CLIENT_ID, SERVER)
client.connect()

client.publish(statetopic,'1',retain=True)
client.set_last_will(statetopic,'0',retain=True)


while True:
	client.set_callback(sub_cb)
	client.subscribe(TOPIC1)

	
