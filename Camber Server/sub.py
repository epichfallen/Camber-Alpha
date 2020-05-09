topics= ["wind/tws","wind/twa","wind/aws,wind/awa,boat/speed,boat/depth,boat/heel"]

import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost",1883,60)


    client.publish("truewind/angle", round(tw.angle,1));
    client.publish("truewind/speed", round(tw.mag,1));
    client.publish("relativewind/speed", round(rw.mag,1));
    client.publish("relativewind/angle", round(rw.angle,1));
    

client.disconnect();
