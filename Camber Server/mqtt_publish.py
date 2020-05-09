import paho.mqtt.client as mqtt
from boat_sim import mqtt_data

client = mqtt.Client()
client.connect("localhost",1883,60)

#sens for sensor input
#sim for simulator input
source="sim"

global devicename
devicename = "Raspberry Server"


while True:
    if source=="sim":
        
        #print(tws.value)
        client.publish("wind/tws", mqtt_data.tws) #true wind speed
        client.publish("wind/twa",mqtt_data.twa) #true wind angle
        
        client.publish("boat/speed", mqtt_data.boat_speed) #boat speed
        


client.disconnect()