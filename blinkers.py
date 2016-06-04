import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import time# BROKER_NAME = "127.0.0.1"
BROKER_NAME = "128.114.63.86"

# AS = "L0", tells the sensor which to base the setpoint off.
# AP = changes the setpoint value.
# AA = "a bool in C. 1 or not 1
# AO = on/off, off forces off.
# AO0=1
publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AO0=1', hostname=BROKER_NAME)
time.sleep(1)
publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AO1=1', hostname=BROKER_NAME)
time.sleep(1)
publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AO2=1', hostname=BROKER_NAME)
time.sleep(1)
# # AP0=50
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", '\x41\x50\x30\x3D\x35\x30\x0A', hostname=BROKER_NAME)
# # AP1=100
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", '\x41\x50\x31\x3D\x31\x30\x30\x0A', hostname=BROKER_NAME)
# # AP2=400
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", '\x41\x50\x32\x3D\x34\x30\x30\x0A', hostname=BROKER_NAME)

# READ
# publish.single("testbed/gateway/mqtt/0013a20040daebd0", '\x52\x45\x41\x44\x0A', hostname=BROKER_NAME)
while(True):
	publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AA0=1', hostname=BROKER_NAME)
	time.sleep(1)
	publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AA1=1', hostname=BROKER_NAME)
	time.sleep(1)
	publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AA2=1', hostname=BROKER_NAME)
	time.sleep(1)
	publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AA0=0', hostname=BROKER_NAME)
	time.sleep(1)
	publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AA1=0', hostname=BROKER_NAME)
	time.sleep(1)
	publish.single("testbed/gateway/mqtt/0013a20040daebd0", 'AA2=0', hostname=BROKER_NAME)
	time.sleep(1)