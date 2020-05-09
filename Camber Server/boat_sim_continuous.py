# -*- coding: utf-8 -*-
"""
Created on Wed May  6 00:22:15 2020

@author: piping,epicfallen
"""

from time import sleep
import random
from wa_calc import vec
from wa_calc import vec_add
from wa_calc import boat_to_compass


#global variables
startspeed = 10 #stable wind speed
tempspeed = startspeed #set the temporary value to start speed
startdepth = 20 #start depth value
tempdepth = startdepth #set the temporary value to start depth
startheel = 20 #start depth value
tempheel = startheel #set the temporary value to start depth
aw_mag_log=[]


def realistic_heading(input):#generate realistic heading data
    max = input + 1
    min = input - 1
    output = random.randint(min,max)
    return output


def realistic_heel(): #generate realistic heel from apparent wind
    return round((aw.mag**1.4)/2,1)
    

def realistic_depth():
    global startdepth
    global tempdepth
    min = startdepth - 10 #shallowest
    max = startdepth + 10 #deepest
    tempdepth = tempdepth + random.randint(-1,1)/5*random.randint(1,3)
    if tempdepth >= max:
        tempdepth = tempdepth - 3
    if tempdepth <= min:
        tempdepth = tempdepth + 3  
    return round(tempdepth,1)


def realistic_aws(): #generate realistic aparent wind speed
    global startspeed
    global tempspeed
    min = startspeed - (startspeed/100)*50 #lows
    max = startspeed + (startspeed/100)*80 #gusts
    tempspeed = tempspeed + random.randint(-1000,1000)/2000
    if tempspeed >= max:
        tempspeed = tempspeed - 3
    if tempspeed <= min:
        tempspeed = tempspeed + 3   
    return tempspeed


def boat_speed(aawm): #boatspeed from average aws
  bs=9.4-9.4*(0.9)**aawm
  return bs


def average_aw_mag(aw): #generate average from the last 5 values of aws
    global aw_mag_log
    tempsum = 0
    aw_mag_log.append(aw)
    if len(aw_mag_log) <= 5:
        return aw
    else:
        for i in aw_mag_log[-5:]:
            tempsum=i+tempsum  
        aw_mag_log=aw_mag_log[-5:] 
        return tempsum/5           



while True:
    aw = vec(realistic_aws(),random.randint(3655,3755)/100)
    aawm = average_aw_mag(aw.mag)
    #aw.mag=aawm
    bs = boat_speed(aawm)
    COG = vec(bs, 180)
    heading = realistic_heading(120)#set the heading
    tw = vec_add(aw,COG)
    sleep(0.15)

    print("TWS:",round(tw.mag,1),"TWA:",round(boat_to_compass(heading,tw.angle),1),"BS",round(bs,1),"AWS:",round(aw.mag,1),"AWA:",round(abs(aw.angle),1))

    print("Depth:", realistic_depth(),"Heel:", realistic_heel())
    print("============================================================")
  
    
    
    
    
    

