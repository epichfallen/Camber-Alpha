import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost",1883,60)

#sens for sensor input
#sim for simulator input
source="sim"

global devicename
devicename = "Raspberry Server"


while True:
    if source=="sim":
        import boat_sim as sim

        client.publish("wind/tws", sim.aw) #true wind speed
        client.publish("wind/twa", sim.twa) #true wind angle
        client.publish("wind/aws", sim.aws) #apparent wind speed
        client.publish("wind/awa", sim.awa) #apparent wind angle
        client.publish("boat/speed", sim.bsr) #boat speed
        client.publish("boat/depth", sim.dpth) #depth
        client.publish("boat/heel", sim.heel) #boat heel


client.disconnect()