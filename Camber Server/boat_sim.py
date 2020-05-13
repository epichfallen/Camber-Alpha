# -*- coding: utf-8 -*-




import mqtt_publish as mqtt
from time import sleep
from wa_calc import *


import datetime


mqtt.connect()




        


   
print("**Simulation Started**")

while True:
    
    aw = vec(realistic_aws(),random.randint(3655,3755)/100)
    aawm = average_aw_mag(aw.mag)
    #aw.mag=aawm
    bs = boat_speed(aawm)
    COG = vec(bs, 180)
    heading = realistic_heading(120)#set the heading
    tw = vec_add(aw,COG)
    sleep(0.1)

   
    tws  = round(tw.mag,1)
    twa  = round(boat_to_compass(heading,tw.angle),1)
    awa  = round(abs(aw.angle),1)
    aws  = round(aw.mag,1)
    bsr  = round(bs,1)
    dpth = realistic_depth()
    heel = realistic_heel(aw)

    time = datetime.datetime.now()
    print(starttime-time)

    mqtt.publish("time/now",time.strftime("%Y-%m-%d %H:%M:%S"))
    mqtt.publish("wind/tws",tws)
    mqtt.publish("wind/twa",twa)
    mqtt.publish("wind/twa to boat",round(tw.angle,1))
    mqtt.publish("wind/aws",aws)
    mqtt.publish("wind/awa",awa)
    mqtt.publish("boat/speed",bsr)
    mqtt.publish("boat/depth",dpth)
    mqtt.publish("boat/heel" ,heel)

  
    
   

    
    

