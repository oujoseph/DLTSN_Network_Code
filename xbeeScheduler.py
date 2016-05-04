# Requirements: mqtt paho library for python installed

import sys
import paho.mqtt.client as mqtt

def on_message(mqttc, obj, msg):
    t = msg.payload.split('\r')[0]
    if float(t) > 26:
        print "ABOVE SETPOINT! Do something."
        # publish.single("test", t, hostname=BROKER_NAME)
# for specific client:
# mqttc = mqtt.Client("client-id")


mqttc = mqtt.Client("Scheduler")
mqttc.on_message = on_message

#debug messages
#mqttc.on_log = on_log

mqttc.connect("127.0.0.1", 1883, 60)
mqttc.subscribe("testbed/0002", 0)
mqttc.loop_forever()
