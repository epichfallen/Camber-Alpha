# -*- coding: utf-8 -*-
import connection as mqtt
from time import sleep
from wa_calc import *
import datetime
import time
import sqlite3

mqtt.connect()

mqtt.publish_retained("display/2fc4f5fc/config","4,0,1,2,3")

# conn=sqlite3.connect("log.db")
# c=conn.cursor()

# c.execute("""CREATE TABLE IF NOT EXISTS logbook (
#                                         latitude real,
#                                         longtitude real,
#                                         tws real,
#                                         twa integer,
#                                         aws real,
#                                         awa integer,
#                                         bs real,
#                                         heel real,
#                                         dpth real,
#                                         heading integer,
#                                         sec_time integer
#                                     )""")

counter_mins = 5
starttime = int(time.time() + counter_mins*60)
mqtt.publish("race/starttime",starttime)


print("**Simulation Started**")
boat_gps=gps_coords(40, 55, 'N', 'E')
while True:
    
    aw = vec(realistic_aws(),random.randint(3355,3755)/100)
    aawm = average_aw_mag(aw.mag)
    #aw.mag=aawm
    bs = boat_speed(aawm)
    COG = vec(bs, 180)
    heading = realistic_heading(120)#set the heading
    tw = vec_add(aw,COG)
    boat_gps=generate_gps(heading, bs, boat_gps)
    sleep(0.3) 

   
    tws  = round(tw.mag,1)
    twa  = round(boat_to_compass(heading,tw.angle),1)
    awa  = round(abs(aw.angle),1)
    aws  = round(aw.mag,1)
    bsr  = round(bs,1)
    dpth = realistic_depth()
    heel = realistic_heel(aw)

    
    
    twawithzero = str(int(tw.angle))
    if len(twawithzero) < 3 :
        twawithzero = "0" + twawithzero
    awawithzero = str(int(awa))
    if len(awawithzero) < 3 :
        awawithzero = "0" + awawithzero
    

    


    # bundle = str(tws) +","+ str(round(tw.angle,1)) +","+ str(aws) +","+ str(awa) +","+ str(bsr) +","+ str(dpth) +","+ str(heel)
    # print (bundle)
    # c.execute("INSERT INTO logbook VALUES (?,?,?,?,?,?,?,?,?,?,?)",(boat_gps.latitude,boat_gps.longtitude,tws,twa,aws,awa,bsr,heel,dpth,heading,int(time.time())))
    # conn.commit() 
    # mqtt.publish("COORDINATES latitude", boat_gps.latitude)
    # mqtt.publish("COORDINATES longtitude", boat_gps.longtitude)

    mqtt.publish("wind/tws",tws)
    mqtt.publish("wind/twa",twawithzero)
    mqtt.publish("wind/aws",str(aws))
    mqtt.publish("wind/awa",awawithzero)
    mqtt.publish("boat/speed",str(bsr))
    mqtt.publish("boat/heel" ,str(heel))
    mqtt.publish("boat/depth",str(dpth))
    mqtt.publish("boat/heading",str(heading))
    
    # mqtt.publish("bundle/all",bundle)
   
    

  
 
# conn.close()

    
    

