import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
BROKER_NAME = "127.0.0.1"

GET_TYPE = '\x54\x3F\x0A'
NODE_DISCOVER_WAIT_DURATION = 10

SEND_ND = 0
state2Counter = 0
State = 1
nodeList = {}
# publish.single("testbed/gateway/mqtt/" + hexstring, '\x54\x3F\x0A', hostname=BROKER_NAME)


# Runs AT command ND, and collects it all into nodeList[]

# Publish a command when the client connects
def on_connect_state1(client, userdata, rc):
    global SEND_ND
    # Only send a node discover the first time on_message1 is called.
    if SEND_ND == 0:
        publish.single("testbed/gateway/mqtt/", 'NODE_DISCOVER', hostname=BROKER_NAME)
        SEND_ND = 1

def on_message_state1(mqttc, obj, msg):
    global State
    global nodeList
    print "In state1 On Message"
    print "message received: " + msg.payload

    # If a received message isn't the end
    # Make an empty dictionary entry for the received message
    # mapping the mac address of an xbee to a dictionary.
    if msg.payload != "END":
    	nodeList[msg.payload] = None
    else:
    	print "Ending State 1 of Node Discovery"
    	State = 2
        mqttc.disconnect()

def state1():
    global SEND_ND
    global State
    SEND_ND = 0
    print "In State 1:"
    mqttc = mqtt.Client("xbeeNodeDiscoverS1")
    mqttc.on_message = on_message_state1
    
    # starts sending messages on connect -- appears to be fast enough to catch all messages.
    mqttc.connect(BROKER_NAME, 1883, NODE_DISCOVER_WAIT_DURATION)
    mqttc.subscribe("testbed/gateway/nodes/", 0)
    mqttc.on_connect = on_connect_state1
    print "starting on_message_state 1:"
    if State == 1:
        mqttc.loop_forever()

def on_connect_state2(client, userdata, rc):
    global nodeList
    global state2Counter
    print "In state2 on connect message"
    for MacAddr in nodeList:
        publish.single("testbed/gateway/mqtt/" + MacAddr, GET_TYPE, hostname=BROKER_NAME)
        # Increment state2counter so on_message_state2 knows when to stop searching
        state2Counter = state2Counter + 1


# Uses nodeList[] for a list of nodes to send a query command to, and wait for response
def on_message_state2(mqttc, obj, msg):
    global state2Counter
    global nodeList
    print "In state2 On Message"

    # msg.topic.split will eventually return the mac address.
    # when this is implemented, we can set nodeList[msg.topic.split("/"[-1])] = queried data.
    
    print "nodelist = "
    print len(nodeList)
    MACfromTopic = msg.topic.split("/")[-1]


    # As state2counter increments before on_message_state2 runs,
    #  we need to check to see if it's less than len(nodeList) + 1
    if state2Counter < (len(nodeList) + 1):
        print "state2counter less than len nodeList"
        print nodeList
        nodeList[MACfromTopic] = None
        print nodeList
    else:
        print "DONE"
        State = 0
        mqttc.disconnect()


def state2():
    global State
    global state2Counter
    # reset the counter
    state2Counter = 0

    mqttc = mqtt.Client("xbeeNodeDiscoverS2")
    mqttc.on_message = on_message_state2
    mqttc.connect(BROKER_NAME, 1883, NODE_DISCOVER_WAIT_DURATION)
    mqttc.subscribe("testbed/gateway/data/#", 0)
    # starts sending messages on connect -- appears to be fast enough to catch all messages.
    mqttc.on_connect = on_connect_state2
    print "Beginning State 2 of Node Discovery"
    if State == 2:
        mqttc.loop_forever()
    print "END PHASE 2"


# Node discover is done in 2 states: collecting mac addresses, and querying each one.
# A 3rd state rearms nodeDiscover to allow it to iterate again.
# on_message() serves main(), and starts 

def on_message(mqttc, obj, msg):
    print "Command received by nodeDiscover Client"
    if msg.payload == "START":
        print "Starting node discovery..."

        # State1 will loop until it disconnects, and will be followed by state2, which does the same
        state1()
        state2()
        print nodeList
        main()

# This part runs first.
# to start it, send message "START" to testbed/nodeDiscover/

def main():
    # Set/reset all variables and states
    global SEND_ND
    global state2Counter
    global State
    global nodeList
    SEND_ND = 0
    state2Counter = 0
    State = 1
    nodeList = {}
    
    mqttc = mqtt.Client("xbeeNodeDiscover")
    mqttc.on_message = on_message
    mqttc.connect(BROKER_NAME, 1883)
    mqttc.subscribe("testbed/nodeDiscover/#", 0)
    mqttc.loop_forever()

if __name__ == "__main__":main()