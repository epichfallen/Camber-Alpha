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

tws  = None #0
twa  = None #1  
twd  = None 
aws  = None #2
awa  = None #3
l_r  = None
bs   = None #4
heel = None #5
ptch = None #6
dpth = None #7
hdg  = None #8
lat  = None
lon  = None
lat_dir = 'N'
lon_dir = 'E'
sog = None
cog = None

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
            boat_vec = vec(bs, 180)
            heading = realistic_heading(120)#set the heading
            tw = vec_add(aw,boat_vec)
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
                if aws != None: #publish to mqtt if not None
                    connection.publish("wind/aws",aws)
            except:
                pass 
            try: #GET AWA DATA
                awa = msg.deg_r 
                l_r = msg.l_r
                print("AWA:" ,awa, l_r)

                if awa != None: #publish to mqtt if not None
                    connection.publish("wind/awa",awa)
            except:
                pass
            
            try: #GET GPS VALUES AND CALCULATE COG AND SOG
                if lat is not None:
                    gps_old = gps_coords(lat,lon,lat_dir,lon_dir)
                    gps_new = gps_coords(float(msg.latitude),float(msg.longitude),msg.lat_dir,msg.lon_dir)
                    sog = SOG(gps_old,gps_new,gps_time,msg.timestamp)
                    cog = COG(gps_old,gps_new)
                    print("COG:",cog)
                    print("SOG:",sog)
                try:
                    lon = float(msg.longitude)
                    lat = float(msg.latitude)
                    lat_dir = msg.lat_dir
                    lon_dir = msg.lon_dir
                    gps_time = msg.timestamp
                except:
                    lon=None
                    lat=None
                    pass      
            except Exception as e:
                # print(e)
                pass
        
            try: #GET DEPTH DATA
                dpth = msg.depth
                print("DPTH:" , dpth)
            except:
                pass

            try: #GET BOAT SPEED DATA
                bs = msg.water_speed_knots
                print("BS:" , bs)
            except:
                pass

            try: #GET HEADING DATA
                hdg = float(msg.heading_magnetic)
                print("HDG:" , hdg)
            except:
                pass
            

            try:
                awa = msg.deg_r 
                aws = msg.wind_speed_kn
                if awa is not None and aws is not None and cog is not None and sog is not None:
                    aw = vec(aws,awa_convert(awa,l_r)) #construct apparent wind vector   
                    csog = vec(sog,180)
                    tw = vec_add(aw,csog)
                    tws  = round(tw.mag,1)
                    twa  = round(tw.angle,1)
                    twd  = TWD(hdg,tw.angle)
                    print("TWS:", tws)
                    print("TWA:", twa)
                    print("TWD:", round(twd,1))


                elif awa is not None and aws is not None and bs is not None and hdg is not None and cog is None:
                    aw = vec(aws,awa) #construct apparent wind vector   
                    bhed = vec(float(bs), float(hdg)) 
                    tw = vec_add(aw,bhed)    
                    tws  = round(tw.mag,1)
                    twa  = round(tw.angle,1)
                    twd  = round(boat_to_compass(hdg,tw.angle),1)
                    print("TWS:", tws) 
                    print("TWA:", twa)
                    print("TWD:", twd)
                    
            except Exception as e:
                print(e)
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

