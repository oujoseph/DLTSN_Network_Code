import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
BROKER_NAME = "127.0.0.1"
# BROKER_NAME = "128.114.63.86"

hexstring = "0013a20040a57a9c"

# while (True):
# 	publish.single("testbed/scheduler/freq", '60.1', hostname=BROKER_NAME)
# 	time.sleep(5)
# 	publish.single("testbed/scheduler/freq", '59.2', hostname=BROKER_NAME)
# 	time.sleep(5)

publish.single("testbed/iterationClient/0013a20040daebd0", 'STOP L0?', hostname=BROKER_NAME)
# publish.single("testbed/iterationClient/0013a20040a57a9c", 'START \x4C\x30\x3F\x0A', hostname=BROKER_NAME)

# publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'READ', hostname=BROKER_NAME)
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AA0=1', hostname=BROKER_NAME)
# time.sleep(1)
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AA1=1', hostname=BROKER_NAME)
# time.sleep(1)
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AA2=1', hostname=BROKER_NAME)
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'READ', hostname=BROKER_NAME)

# publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'READ', hostname=BROKER_NAME)

# publish.single("testbed/gateway/mqtt/" + hexstring, '\x54\x3F\x0A', hostname=BROKER_NAME)

# publish.single("testbed/gateway/mqtt/0013a20040a57a9c", '\x44\x48\x30\x3F\x0A', hostname=BROKER_NAME)

# publish.single("testbed/nodeDiscover/command/", 'START', hostname=BROKER_NAME)

# publish.single("testbed/gateway/mqtt/", 'NODE_DISCOVER', hostname=BROKER_NAME)

# publish.single("testbed/iterationClient/0013a20040a57a9c", 'STOP DH0?', hostname=BROKER_NAME)
# publish.single("testbed/iterationClient/0013a20040a57a9c", 'STOP DT0?', hostname=BROKER_NAME)
# publish.single("testbed/iterationClient/0013a20040a57a9c", 'STOP \x44\x48\x30\x3F\x0A')
# publish.single("testbed/iterationClient/0013a20040daebd0", 'START \x4C\x30\x3F\x0A')
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'READ', hostname=BROKER_NAME)
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", '\x52\x45\x41\x44\x0A', hostname=BROKER_NAME)
# AS = "L0", tells the sensor which to base the setpoint off.
# AP = changes the setpoint value.
# AA = "a bool in C. 1 or not 1" Turn on force on (but gets overridden by AO=0)
# AO = on/off, off forces off.
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AP0=3', hostname=BROKER_NAME)

# AO0=1
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", '\x41\x4F\x30\x3D\x31\x0A', hostname=BROKER_NAME)
# AO1=1
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", '\x41\x4F\x31\x3D\x31\x0A', hostname=BROKER_NAME)
# AO2=1
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", '\x41\x4F\x32\x3D\x31\x0A', hostname=BROKER_NAME)

# AP0=50
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", '\x41\x50\x30\x3D\x35\x30\x0A', hostname=BROKER_NAME)
# AP1=100
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", '\x41\x50\x31\x3D\x31\x30\x30\x0A', hostname=BROKER_NAME)
# AP2=400
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", '\x41\x50\x32\x3D\x34\x30\x30\x0A', hostname=BROKER_NAME)

# READ
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", '\x52\x45\x41\x44\x0A', hostname=BROKER_NAME)