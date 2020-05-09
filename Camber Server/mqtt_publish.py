import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost",1883,60)


def connect():
    client = mqtt.Client()
    client.connect("localhost",1883,60)

def publish(t,d):
    client.publish(t,d)

