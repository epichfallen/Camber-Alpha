import pynmea2
import serial
import io
import connection
from wa_calc import *
import datetime
import time
from time import sleep

connection.connect()


ser = serial.Serial('COM7', 115200, timeout=0.1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

tws  = 0 #0
twa  = 0 #1  
aws  = 0 #2
awa  = 0 #3
bs   = 0 #4
heel = 0 #5
ptch = 0 #6
dpth = 0 #7
hdg  = 0 #8
lat  = 0
lon  = 0
lat_dir = 'N'
lon_dir = 'E'
sog = 0
cog = 0

timenow = int(time.time())
gps_time = datetime.time()


while True:

    if (connection.serverconfig.input == 0):# Simulator
        connection.connect()
        connection.publish_retained("display/2fc4f5fc/config","4,0,1,2,3")

        counter_mins = 5
        starttime = int(time.time() + counter_mins*60)
        connection.publish("race/starttime",starttime)

        print("**Simulation Started**")
        boat_gps=gps_coords(40, 55, 'N', 'E')

        while (connection.serverconfig.input == 0):

            aw = vec(realistic_aws(),random.randint(3355,3755)/100)
            aawm = average_aw_mag(aw.mag)
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

            connection.publish("COORDINATES latitude", boat_gps.latitude)
            connection.publish("COORDINATES longtitude", boat_gps.longtitude)
            connection.publish("wind/tws",tws)
            connection.publish("wind/twa",twawithzero)
            connection.publish("wind/aws",str(aws))
            connection.publish("wind/awa",awawithzero)
            connection.publish("boat/speed",str(bsr))
            connection.publish("boat/heel" ,str(heel))
            connection.publish("boat/depth",str(dpth))
            connection.publish("boat/heading",str(heading))
    
    #==============================================================#
             
    if (connection.serverconfig.input == 1): #NMEA 0183 

        conn=sqlite3.connect("log.db") # access the database 
        c=conn.cursor() 

        try:
            line = sio.readline()
            msg = pynmea2.parse(line)
            # print(line)
            
            try: # GET AWS DATA
                aws = msg.wind_speed_kn
                print("AWS:" , aws)
                if aws != 0: #publish to mqtt if not 0
                    connection.publish("wind/aws",aws)
            except:
                aws = 0
                pass 
            try: #GET AWA DATA
                awa = msg.deg_r 
                print("AWA:" ,awa)
                if awa != 0: #publish to mqtt if not 0
                    connection.publish("wind/awa",awa)
            except:
                awa = 0
                pass
            
            try: #GET GPS VALUES AND CALCULATE COG AND SOG
                if lat != 0:
                    gps_old = gps_coords(lat,lon,lat_dir,lon_dir)
                    gps_new = gps_coords(float(msg.latitude),float(msg.longitude),msg.lat_dir,msg.lon_dir)
                    sog = SOG(gps_old,gps_new,gps_time,msg.timestamp)
                    cog = COG(gps_old,gps_new)
                    print("COG:",cog)
                    print("SOG:",sog)
                lon = float(msg.longitude)
                lat = float(msg.latitude)
                lat_dir = msg.lat_dir
                lon_dir = msg.lon_dir
                gps_time = msg.timestamp
                
            except Exception as e:
                # print(e)
                pass
        
            try: #GET DEPTH DATA
                dpth = msg.depth
                print("Depth:" , dpth)
            except:
                pass

            try: #GET BOAT SPEED DATA
                bs = msg.water_speed_knots
                print("BS:" , bs)
            except:
                pass

            try: #GET HEADING DATA
                hdg = msg.heading_magnetic
                print("HDG:" , hdg)
            except:
                pass
            
            try: #CALCULATE TWS,TWA,TWD USING GPS AND APPARENT WIND
                if awa,aws!=0:
                aw = vec(aws,awa) #construct apparent wind vector   
                csog = vec(sog, cog)
                tw = vec_add(aw,csog)    
                tws  = round(tw.mag,1)
                twa  = round(tw.angle,1)
                print("TWS:", tws)
                print("TWA:", twa)
            except:
                pass
            
            

            print("========")

            

            # print(repr(msg))

            # if int(time.time()) - timenow >= 1:
            #     c.execute("INSERT INTO logbook VALUES (?,?,?,?,?,?,?,?,?,?,?)",(lat,lon,tws,twa,aws,awa,bsr,heel,dpth,heading,int(time.time())))
            #     time = int(time.time())
        except serial.SerialException as e:
            print('Device error: {}'.format(e))
            break
        except pynmea2.ParseError as e:
            # print('Parse error: {}'.format(e))
            continue

