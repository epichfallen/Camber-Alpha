import paho.mqtt.client as mqtt



class serverconfig: #create class for server config data
    def __init__(self,input):
        self.input=input

serverconfig.input = 0  #get from local db


def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    if msg.topic == "server/config/input":
        if msg.payload == "0":
            serverconfig.input = 0
        if msg.payload == "1":
            serverconfig.input = 1
        if msg.payload == "2":
            serverconfig.input = 2       
    print(msg.topic+" "+str(msg.payload))

 

client = mqtt.Client()
client.on_message = on_message
client.connect("192.168.1.46",1883,60)
client.subscribe("server/config/#",0)
client.loop_start()


def connect():
    client = mqtt.Client()
    client.connect("192.168.1.46",1883,60)

def publish_retained(t,d):
    client.publish(t, d, qos=0, retain=True)

def publish(t,d):
    client.publish(t,d)

