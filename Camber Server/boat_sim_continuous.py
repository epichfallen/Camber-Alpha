# -*- coding: utf-8 -*-
"""
Created on Wed May  6 00:22:15 2020

@author: piping,epicfallen
"""

from time import sleep
import random
from wa_calc import vec
from wa_calc import vec_add

#global variables
startspeed = 10 #stable wind speed
tempspeed = startspeed #set the temporary value to start speed
aw_mag_log=[]

def realistic_aws():
    global startspeed
    global tempspeed

    min = startspeed - (startspeed/100)*50 #lows
    max = startspeed + (startspeed/100)*80 #gusts

    tempspeed = tempspeed + random.randint(-1000,1000)/1000

    if tempspeed >= max:
        tempspeed = tempspeed - 0.5
    if tempspeed <= min:
        tempspeed = tempspeed + 0.5   
    
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
    aw.mag=aawm
    bs = boat_speed(aawm)
    COG = vec(bs, 180)
    
    tw = vec_add(aw,COG)
    sleep(0.15)
    print("TWS:",round(tw.mag,1),"TWA:",round(tw.angle,1),"BS",round(bs,1),"AWS:",round(aw.mag,1),"AWA:",round(aw.angle,1))
  
    
    
    
    
    

