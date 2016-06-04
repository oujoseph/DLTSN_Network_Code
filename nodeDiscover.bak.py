import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading
import time
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

def on_message_state1(client1, obj, msg):
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
        client1.disconnect()

def state1():
    global SEND_ND
    global State
    SEND_ND = 0
    print "In State 1:"
    client1 = mqtt.Client("xbeeNodeDiscoverS1")
    client1.on_message = on_message_state1
    
    # starts sending messages on connect -- appears to be fast enough to catch all messages.
    client1.connect(BROKER_NAME, 1883, NODE_DISCOVER_WAIT_DURATION)
    client1.subscribe("testbed/gateway/nodes/", 0)
    client1.on_connect = on_connect_state1
    print "starting on_message_state 1:"
    if State == 1:
        client1.loop_forever()

def on_connect_state2(client2, userdata, rc):
    global nodeList
    global state2Counter
    print "In state2 on connect message"
    for MacAddr in nodeList:
        print MacAddr
        publish.single("testbed/gateway/mqtt/" + MacAddr, GET_TYPE, hostname=BROKER_NAME)
        # Increment state2counter so on_message_state2 knows when to stop searching
        state2Counter = state2Counter + 1
    # Disconnect after messages are sent
    print "Disconnecting"
    client2.disconnect()
# Uses nodeList[] for a list of nodes to send a query command to, and wait for response
def on_message_state2(client, obj, msg):
    global State
    global nodeList
    print "IN ON_MESSAGE_STATE"
    if State == 0:
        client.disconnect()
        return
    # msg.topic.split will eventually return the mac address.
    # when this is implemented, we can set nodeList[msg.topic.split("/"[-1])] = queried data.
    MACfromTopic = msg.topic.split("/")[-1]
    if MACfromTopic not in nodeList:
        State = 0
        print "ATTEMPTING TO ADD A NON-ELEMENT OF nodeList"
        client.disconnect()
        return
    nodeList[MACfromTopic] = msg.payload
    print nodeList
    print "Reached end of on_message_state2"
    client.disconnect()

# def state2():
#     global State
#     global state2Counter
#     # reset the counter
#     state2Counter = 0

#     client = mqtt.Client("xbeeNodeDiscoverS2")
#     client.on_message = on_message_state2
#     client.connect(BROKER_NAME, 1883, NODE_DISCOVER_WAIT_DURATION)
#     client.subscribe("testbed/gateway/data/#", 0)
#     # starts sending messages on connect -- appears to be fast enough to catch all messages.
#     client.on_connect = on_connect_state2
#     print "Beginning State 2 of Node Discovery"
#     if State == 2:
#         client.loop(2,10)
#     print "END PHASE 2"
#     client.disconnect()

def send_state2():
    print "IN send_state2"
    client2 = mqtt.Client("xbeeNodeDiscoverS2send")
    client2.connect(BROKER_NAME, 1883, NODE_DISCOVER_WAIT_DURATION)
    client2.on_connect = on_connect_state2
    client2.loop()
    print "out of send_state2()"

def receive_state2():
    global state2Counter
    global nodeList

    state2Counter = 0
    print "IN receive_state2"
    client = mqtt.Client("xbeeNodeDiscoverS2receive")
    client.connect(BROKER_NAME, 1883, 60)
    client.subscribe("testbed/gateway/data/#", 0)
    client.on_message = on_message_state2
    while state2Counter < (len(nodeList) + 1):
        print "in client loop"
        client.loop_forever()
        state2Counter = state2Counter + 1
        print "incremented client for client loop"
    print "out of client loop"
    client.disconnect()
# 2 threads so can break out of scanning if nothing is found after a certain duration of time
# client.loop(timeout=X) doesn't work
def state2():
    global state2Counter
    state2Counter = 0
    if State == 2:
        receive = threading.Thread(target=receive_state2)
        send = threading.Thread(target=send_state2)
        send.start()
        receive.start()
        time.sleep(NODE_DISCOVER_WAIT_DURATION)
        print "done waiting."
        send.join()
        print "joining send"
        receive.join()
        print "joining receive"

# Node discover is done in 2 states: collecting mac addresses, and querying each one.
# A 3rd state rearms nodeDiscover to allow it to iterate again.
# on_message() serves main(), and starts 

def on_message(client, obj, msg):
    print "Command received by nodeDiscover Client"
    if msg.payload == "START":
        print "Starting node discovery..."

        # State1 will loop until it disconnects, and will be followed by state2, which does the same
        state1()
        state2()
        print "-------END OF STATE 1 AND 2-------"
        print nodeList
        main()

# This part runs first.
# to start it, send message "START" to testbed/nodeDiscover/

def on_connect(client,obj,msg):
    pass

def main():
    print "\n\n--IN MAIN--\n"
    # Set/reset all variables and states
    global SEND_ND
    global state2Counter
    global State
    global nodeList
    SEND_ND = 0
    state2Counter = 0
    State = 1
    nodeList.clear()
    
    client = mqtt.Client("xbeeNodeDiscover")
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(BROKER_NAME, 1883)
    client.subscribe("testbed/nodeDiscover/#", 0)
    client.loop_forever()

if __name__ == "__main__":main()