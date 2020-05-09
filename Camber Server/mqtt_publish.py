import paho.mqtt.publish as publish

#sens for sensor input
#sim for simulator input
source=sim
global devicename
devicename = "Raspberry Server"

if source==sim:
    import boat_sim_continuous
    publish.single("wind/tws", round(tw.mag,1), hostname=devicename) #true wind speed
    publish.single("wind/twa", round(boat_to_compass(heading,tw.angle),1), hostname=devicename) #true wind angle
    publish.single("wind/aws", round(aw.mag,1), hostname=devicename) #apparent wind speed
    publish.single("wind/awa", round(abs(aw.angle),1), hostname=devicename) #apparent wind angle
    publish.single("boat/speed", round(bs,1), hostname=devicename) #boat speed
    publish.single("boat/depth", realistic_depth(), hostname=devicename) #depth
    publish.single("boat/heel", realistic_heel(), hostname=devicename) #boat heel


