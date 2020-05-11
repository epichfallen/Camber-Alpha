# -*- coding: utf-8 -*-
"""
Created on Wed May  6 00:22:15 2020

@author: piping
"""

import math
class gps_coordinate:
    def __init__(self,la,longt):
        self.latitude=la
        self.longtitude=longt
        
        
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

def boat_to_compass(boat_heading,twa):
    tw_bearing=boat_heading+twa
    if tw_bearing>=360:
        return tw_bearing-360
    elif tw_bearing<=0:
        return tw_bearing+360
    else:
        return tw_bearing

def pars_gps_data(gpsdata):
    data=gpsdata.split(",")
    str_latitude_min=''
    str_latitude_deg=''
    str_longtitude_min=''
    str_longtitude_deg=''
    if data[0]=="$GPRMC" and data[2]=="A":
        for i in data[3]:
            if i==".":
                for j in range(i-2,i+2):
                    str_longtitude_min+=j
                break
        lat_deg_temp=data[3]-str_latitude_min
        str_latitude_deg+=lat_deg_temp
        float_lat_deg=float(str_latitude_deg)+float(str_latitude_min)/60
        for i in data[3]:
            if i==".":
                for j in range(i-2,i+2):
                    str_longtitude_min+=j
                break
        longt_deg_temp=data[3]-str_longtitude_min
        str_longtitude_deg+=longt_deg_temp
        float_longt_deg=float(str_longtitude_deg)+float(str_longtitude_min)/60
        return gps_coordinate(float_lat_deg, float_longt_deg)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    