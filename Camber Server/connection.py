import paho.mqtt.client as mqtt
import sqlite3

localserver = "192.168.1.26"

class serverconfig: #create class for server config data
    def __init__(self,input):
        self.input=input


#============= DATABASE INITIALISATION ==========

conn=sqlite3.connect("log.db")
c=conn.cursor()

#Create tables if not found
c.execute("""CREATE TABLE IF NOT EXISTS logbook (
                                        ID INT PRIMARY KEY,
                                        latitude real,
                                        longtitude real,
                                        tws real,
                                        twa integer,
                                        aws real,
                                        awa integer,
                                        bs real,
                                        heel real,
                                        dpth real,
                                        heading integer,
                                        sec_time integer
                                    )""")

c.execute("""CREATE TABLE IF NOT EXISTS serverconfig (
                                        input integer
                                    )""")      



c.execute("SELECT * FROM serverconfig")
row = c.fetchone()
if row:
    print("Found!",row[0])
    serverconfig.input = row[0]
else:
    print("Not found...")
    c.execute("INSERT INTO serverconfig VALUES (?)",("0"))
    serverconfig.input = 0
    


#============== DATABASE INITIALISATION END =============



def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    if msg.topic == "server/config/input":
        conn=sqlite3.connect("log.db")
        c=conn.cursor()
        if msg.payload == "0":
            serverconfig.input = 0
            c.execute("UPDATE serverconfig SET input=0")
        if msg.payload == "1":
            serverconfig.input = 1
            c.execute("UPDATE serverconfig SET input=1")
        if msg.payload == "2":
            serverconfig.input = 2       
            c.execute("UPDATE serverconfig SET input=2") 
        conn.commit()    
        conn.close()
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_message = on_message
client.connect(localserver,1883,60)
client.subscribe("server/config/#",0)
client.loop_start()


def connect():
    client = mqtt.Client()
    client.connect(localserver,1883,60)

def publish_retained(t,d):
    client.publish(t, d, qos=0, retain=True)

def publish(t,d):
    client.publish(t,d)

