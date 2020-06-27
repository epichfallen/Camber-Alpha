import pynmea2
import serial
import io
import pymongo

# #===================== DATABASE INITIALISATION ==========
# import sqlite3
# from sqlite3 import Error


# def create_connection(db_file):
#     """ create a database connection to a SQLite database """
#     conn = None
#     try:
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()

# def create_table(conn, create_table_sql):
#     """ create a table from the create_table_sql statement
#     :param conn: Connection object
#     :param create_table_sql: a CREATE TABLE statement
#     :return:
#     """
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)


# def main():
#     database = r"C:\Users\dunya\Desktop\pythonsqlite.db"

#     conn = sqlite3.connect(database)
#     cursor = conn.cursor()

#     sql_create_config_table = """ CREATE TABLE IF NOT EXISTS serverconfig (
#                                         id integer PRIMARY KEY,
#                                         input integer NOT NULL
#                                     ); """

    

#     # create tables
#     if conn is not None:
#         # create projects table
#         create_table(conn, sql_create_config_table)
#     else:
#         print("Error! cannot create the database connection.")
#     if cursor.execute("select count(*) from serverconfig") > 0:
#         print("yesss")




# if __name__ == '__main__':
#     main()

# #===================== DATABASE INITIALISATION END =================



import mqtt_publish as mqtt
mqtt.connect()

ser = serial.Serial('COM7', 115200, timeout=0.1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))


awa  = 0
aws  = 0
bs   = 0
dpth = 0
lat  = 0
lon  = 0


while 1:
    try:
        line = sio.readline()
        msg = pynmea2.parse(line)
        # print(line)

        try: #try to get awa data if available else pass
            awa = msg.deg_r 
            print("AWA:" ,awa)
            if awa != 0: #publish to mqtt if not 0
                mqtt.publish("wind/awa",awa)
        except:
            pass
        try: 
            aws = msg.wind_speed_kn
            print("AWS:" , aws)
            if aws != 0: #publish to mqtt if not 0
                mqtt.publish("wind/aws",aws)
        except:
            pass 
        try: 
            lat = msg.lat
            print("Latidute:" , lat)
        except:
            pass
        try: 
            dpth = msg.depth
            print("Depth:" , dpth)
        except:
            pass
           
        # print(mqtt.serverconfig.input)
        # print(repr(msg))
    
        
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:
        # print('Parse error: {}'.format(e))
        continue