import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
BROKER_NAME = "127.0.0.1"

hexstring = "0013a20040a57a9c"
# publish.single("testbed/gateway/mqtt/" + hexstring, '\x54\x3F\x0A', hostname=BROKER_NAME)

# publish.single("testbed/gateway/mqtt/", 'NODE_DISCOVER', hostname=BROKER_NAME)

publish.single("testbed/nodeDiscover/", 'START', hostname=BROKER_NAME)

# publish.single("testbed/gateway/mqtt/", 'NODE_DISCOVER', hostname=BROKER_NAME)