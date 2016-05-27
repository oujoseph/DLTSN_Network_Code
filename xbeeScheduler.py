def on_message(mqttc, obj, msg):
    t = msg.payload.split('\r')[0]
    if float(t) > 26:
        print "ABOVE SETPOINT! Do something."
        # publish.single("test", t, hostname=BROKER_NAME)
# for specific client:
# mqttc = mqtt.Client("client-id")


# ND:T=1:H1=23.512

mqttc = mqtt.Client("Scheduler")
mqttc.on_message = on_message

#debug messages
#mqttc.on_log = on_log

mqttc.connect("127.0.0.1", 1883, 60)
mqttc.subscribe("testbed/0002", 0)
mqttc.loop_forever()


import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
BROKER_NAME = "127.0.0.1"

hexstring = "0013a20040a57a9c"
# publish.single("testbed/gateway/mqtt/" + hexstring, '\x54\x3F\x0A', hostname=BROKER_NAME)

# publish.single("testbed/gateway/mqtt/", 'NODE_DISCOVER', hostname=BROKER_NAME)

publish.single("testbed/nodeDiscover/", 'START', hostname=BROKER_NAME)

# publish.single("testbed/gateway/mqtt/", 'NODE_DISCOVER', hostname=BROKER_NAME)