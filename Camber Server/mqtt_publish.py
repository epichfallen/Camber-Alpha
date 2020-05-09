import paho.mqtt.publish as publish

#sens for sensor input
#sim for simulator input
source="sim"

global devicename
devicename = "Raspberry Server"

if source=="sim":
    import boat_sim as sim
    publish.single("wind/tws", sim.aw, hostname=devicename) #true wind speed
    publish.single("wind/twa", sim.twa, hostname=devicename) #true wind angle
    publish.single("wind/aws", sim.aws, hostname=devicename) #apparent wind speed
    publish.single("wind/awa", sim.awa, hostname=devicename) #apparent wind angle
    publish.single("boat/speed", sim.bsr, hostname=devicename) #boat speed
    publish.single("boat/depth", sim.dpth, hostname=devicename) #depth
    publish.single("boat/heel", sim.heel, hostname=devicename) #boat heel


