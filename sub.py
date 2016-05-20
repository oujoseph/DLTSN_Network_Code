# Requirements: mqtt paho library for python installed
import time
import sys
import paho.mqtt.client as mqtt
x = 0

def on_message(mqttc, obj, msg):
    print "TOPIC:" + msg.topic
    print "nonhex : " + msg.payload
    global x
    x = x+1
    print x
# for specific client:
# mqttc = mqtt.Client("client-id")


mqttc = mqtt.Client()
mqttc.on_message = on_message

#debug messages
#mqttc.on_log = on_log

mqttc.connect("127.0.0.1", 1883, 60)
mqttc.subscribe("testbed/gateway/data/#", 0)
# mqttc.subscribe("#", 0)
mqttc.loop_start()
time.sleep(500)
# mqttc.loop_stop(force=False)