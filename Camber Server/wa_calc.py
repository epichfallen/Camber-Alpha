# -*- coding: utf-8 -*-
"""
Created on Wed May  6 00:22:15 2020

@author: piping
"""

import math
import pynmea2
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
    #radius of the earth in km
    r=6371
    lat_dif=degrees_to_radian(gps1.latitude-gps2.latitude)
    long_dif=degrees_to_radian(gps1.longtitude-gps2.longtitude)
    lat1=degrees_to_radian(gps1.latitude)
    lat2=degrees_to_radian(gps2.latitude)
    
    return 2*r*math.asin(math.sqrt((math.sin(lat_dif/2)**2)+math.cos(lat1)*math.cos(lat2)*(math.sin(long_dif/2)**2)))





    
    