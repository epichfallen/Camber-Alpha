import paho.mqtt.client as mqtt
from boat_sim import data

client = mqtt.Client()
client.connect("localhost",1883,60)

#sens for sensor input
#sim for simulator input
source="sim"

global devicename
devicename = "Raspberry Server"


while True:
    if source=="sim":
        
        print(tws.value)
        client.publish("wind/tws", aw.value) #true wind speed
        client.publish("wind/twa", twa.value) #true wind angle
        client.publish("wind/aws", aws.value) #apparent wind speed
        client.publish("wind/awa", awa.value) #apparent wind angle
        client.publish("boat/speed", bsr.value) #boat speed
        client.publish("boat/depth", dpth.value) #depth
        client.publish("boat/heel", heel.value) #boat heel


client.disconnect()