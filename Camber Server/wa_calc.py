# -*- coding: utf-8 -*-

import math
import pynmea2
import random
from global_variables import *
import sqlite3





class vec:
    def __init__(self,mag,angle):
        self.mag=mag
        self.angle=angle


def degrees_to_radian(angle_deg):
    return angle_deg*(math.pi/180)
        

def radian_to_degrees(angle_rad):
    return angle_rad*(180/math.pi)
        
    
def vec_add( vec1, vec2):
    vec1x=vec1.mag*math.cos(degrees_to_radian(vec1.angle))
    vec1y=vec1.mag*math.sin(degrees_to_radian(vec1.angle))
    #calculating x and y components of vectors vector_magnitude*cos(degree)==vector.x 
    vec2x=vec2.mag*math.cos(degrees_to_radian(vec2.angle))
    vec2y=vec2.mag*math.sin(degrees_to_radian(vec2.angle))
    
    vec3x=vec1x+vec2x
    vec3y=vec1y+vec2y
    
    vec3mag=math.sqrt((vec3x**2)+(vec3y**2))
    if vec1.angle==0:
        vec3angle=0
    else:
        vec3angle=math.atan2(vec3y,vec3x)
    vec3=vec(vec3mag,radian_to_degrees(vec3angle))
    return vec3

#boat_to_compass takes degrees not radian and converts it to compass bearing,note that twa is taken inverted as not where it
#directs but as where it comes from
def boat_to_compass(boat_heading,twa):
    tw_bearing=boat_heading+twa
    if tw_bearing>=360:
        return tw_bearing-360
    elif tw_bearing<=0:
        return tw_bearing+360
    else:
        return tw_bearing
    
class gps_coords:
    def __init__(self,lat,longt,lat_dir,long_dir):
        self.latitude=lat
        self.longtitude=longt
        self.latitude_dir=lat_dir
        self.longtitude_dir=long_dir

def gps_parser(gps_data):
    parsed_data=pynmea2.parse(gps_data)
    return gps_coords(pynmea2.dm_to_sd(parsed_data.lat), pynmea2.dm_to_sd(parsed_data.lon),parsed_data.lat_dir,parsed_data.lon_dir)
    



#distance between 2 gps points on earth using haversine formula
#needs to be tested with more sample
def distance_between_twogps(gps1,gps2):
    #radius of the earth in meters
    r=6371e3
    if gps1.latitude_dir!=gps2.latitude_dir:
        lat_dif=degrees_to_radian(gps1.latitude+gps2.latitude)
    else:
        lat_dif=degrees_to_radian(abs(gps1.latitude-gps2.latitude))
    
    if gps1.longtitude_dir!=gps2.longtitude_dir:
        long_dif=degrees_to_radian(gps1.longtitude+gps2.longtitude)
        
    else:
        long_dif=degrees_to_radian(abs(gps1.longtitude-gps2.longtitude))
        
    lat1=degrees_to_radian(gps1.latitude)
    lat2=degrees_to_radian(gps2.latitude)
    
    return 2*r*math.asin(math.sqrt((math.sin(lat_dif/2)**2)+math.cos(lat1)*math.cos(lat2)*(math.sin(long_dif/2)**2)))


def SOG(gps1,gps2,gps_time1,gps_time2):
    date = datetime.date(1, 1, 1)
    datetime1 = datetime.datetime.combine(date, gps_time1)
    datetime2 = datetime.datetime.combine(date, gps_time2)
    time_elapsed = datetime2 - datetime1
    if time_elapsed.total_seconds() != 0:
        return round(distance_between_twogps(gps1,gps2)/(time_elapsed.total_seconds())*3.6/1.86,1)
    else:
        return 0

def realistic_heading(input):#generate realistic heading data
    max = input + 1
    min = input - 1
    output = random.randint(min,max)
    return output


def realistic_heel(aw): #generate realistic heel from apparent wind
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

def eta_to_startline(gpsline1,gpsline2,gps_boat):
    global to_line
    
    global epoch_time_etaline
    #first finding the shift between truewind and line(in an optimal startline truewind is perpendicular to the line)
    #gonna use arctan2 to find the angle of the line according to compass coordinate system
    
    #these are lines of the triangle gpsline1 being the committee boat and gpsline2 being the portside buoy
    line1=gpsline1.latitude-gpsline2.latitude
    line2=gpsline1.longtitude-gpsline2-longtitude
    #length of the line in meters
    len_line=distance_between_twogps(line1, line2)
    #distance between the boat and the portside of the startline and to comittee
    boat_to_buoy=distance_between_twogps(line2, gps_boat)
    boat_to_comittee=distance_between_twogps(line1, gps_boat)
    #now going to use the formula called "Heron's formula" to calculate the perpendicular line to the
    #startline from the boat
    s=(boat_to_comittee+boat_to_buoy+len_line)/2
    distance=(2*math.sqrt(s*(s-boat_to_comittee)*(s-boat_to_buoy)*(s-len_line)))/2
    timestamp=int(time.time())
    
    if epoch_time_etaline==0:
        epoch_time_etaline=timestamp
        to_line=distance
        return 0
    else:
        delta_distance=to_line-distance
        delta_time=timestamp-epoch_time_etaline
        speed=delta_distance/delta_time
        eta_in_seconds=distance/speed
        epoch_time_etaline=int(time.time())
        to_line=distance
        return eta_in_seconds

def generate_gps(heading,boatspd,gps_boat):
    r=6371e3 #radius of earth in meters
    global epoch_time_gpsgen
    boat_latmag=0 #going to be the new latitude after moving in iteration
    boat_lonmag=0 # new longtitude
    boatspdm=(boatspd*1.85)/3.6 #boatspeed translated to m/s from nauticalmile/h aka Knots
    delta_time=0
    distance_taken=0 
    timestamp=int(time.time())
    if epoch_time_gpsgen==0:
        epoch_time_gpsgen=timestamp
        return gps_boat
    else:
        delta_time=timestamp-epoch_time_gpsgen
        distance_taken=boatspdm*delta_time
    distancelat=abs(distance_taken*math.cos(degrees_to_radian(heading))) #distance taken in north-south direction
    distancelon=abs(distance_taken*math.sin(degrees_to_radian(heading)))
    if heading<90 or heading>270:
        if gps_boat.latitude_dir=='N':
            boat_latmag=degrees_to_radian(gps_boat.latitude)+(distancelat/r)
        elif gps_boat.latitude_dir=='S':
            boat_latmag=degrees_to_radian(gps_boat.latitude)-(distancelat/r)
    elif heading>90 and heading<270:
         if gps_boat.latitude_dir=='N':
            boat_latmag=degrees_to_radian(gps_boat.latitude)-(distancelat/r)
         elif gps_boat.latitude_dir=='S':
            boat_latmag=degrees_to_radian(gps_boat.latitude)+(distancelat/r)
    boat_latmag=radian_to_degrees(boat_latmag)
    #these are distances per 1 longtitude degrees at designated latitude
    distance_lon1=distance_between_twogps(gps_boat,gps_coords(gps_boat.latitude, gps_boat.longtitude-1, gps_boat.latitude_dir, gps_boat.longtitude_dir))
    distance_lon2=distance_between_twogps(gps_coords(boat_latmag,gps_boat.longtitude,gps_boat.latitude_dir,gps_boat.longtitude_dir)
                                          , gps_coords(boat_latmag,gps_boat.longtitude-1,gps_boat.latitude_dir,gps_boat.longtitude_dir))
    distance_ave=(distance_lon1+distance_lon2)/2
    if heading>180 and heading<360:
        if gps_boat.longtitude_dir=='W':
            boat_lonmag=gps_boat.longtitude+(distancelon/distance_ave)
        elif gps_boat.longtitude_dir=='E':
            boat_lonmag=gps_boat.longtitude-(distancelon/distance_ave)
    elif heading<180:
        if gps_boat.longtitude_dir=='W':
            boat_lonmag=gps_boat.longtitude-(distancelon/distance_ave)
        elif gps_boat.longtitude_dir=='E':
            boat_lonmag=gps_boat.longtitude+(distancelon/distance_ave)
    return gps_coords(boat_latmag, boat_lonmag, gps_boat.latitude_dir, gps_boat.longtitude_dir)
        
    
            
            
             
        
    
    
    
    
    
    
    
    
    
    
    

    
    