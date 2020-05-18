# -*- coding: utf-8 -*-

import time
import datetime
#global variables
startspeed = 10 #stable wind speed
tempspeed = startspeed #set the temporary value to start speed
startdepth = 20 #start depth value
tempdepth = startdepth #set the temporary value to start depth
startheel = 20 #start depth value
tempheel = startheel #set the temporary value to start depth
aw_mag_log=[]
#time = datetime.datetime.now()
#starttime = time + datetime.timedelta(minutes=5)
to_line=0 #distance between the boat and the startline needed to see the change
epoch_time_etaline=0 #time since epoch in seconds needed to calculate the approach speed to the distance will be added soon
epoch_time_gpsgen=0#time since epoch in seconds needed to calculate gps coordinate change for gps generator