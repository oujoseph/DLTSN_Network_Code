import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
# BROKER_NAME = "127.0.0.1"
BROKER_NAME = "128.114.63.86"

hexstring = "0013a20040a57a9c"
# publish.single("testbed/gateway/mqtt/" + hexstring, '\x54\x3F\x0A', hostname=BROKER_NAME)

# publish.single("testbed/gateway/mqtt/0013a20040a57a9c", '\x44\x48\x30\x3F\x0A', hostname=BROKER_NAME)

publish.single("testbed/nodeDiscover/command/", 'START', hostname=BROKER_NAME)

# publish.single("testbed/gateway/mqtt/", 'NODE_DISCOVER', hostname=BROKER_NAME)
# publish.single("testbed/iterationClient/0013a20040a57a9c", 'START \x44\x48\x30\x3F\x0A')
# publish.single("testbed/iterationClient/0013a20040a57a9c", 'STOP \x44\x48\x30\x3F\x0A')
# publish.single("testbed/iterationClient/0013a20040daebd0", 'START \x4C\x30\x3F\x0A')