# Triple threaded implementation of a scheduler client:
# freqThread() updates frequency value
# Constantly reads testbed/scheduler/freq/

# iterate() iterates through the nodelist when a new frequency value is received


# nd() sends node discover messages continuously every X seconds

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading
import time


stableFreq = 60.0
BROKER_NAME = "128.114.63.86"
nodeList = {}
contingency = 0

def onUpdate_freq(mqttc, obj, msg):
	global contingency

	print "in onUpdate_freq"

	newFreq = float(msg.payload)
	if newFreq == stableFreq:
		contingency = 0
	
	if newFreq > (stableFreq):
		print "newFreq > stableFreq"
		if newFreq < (stableFreq + 1.0):
			contingency = 4
		if newFreq < (stableFreq + 0.1):
			contingency = 3
		if newFreq < (stableFreq + 0.01):
			contingency = 2
		if newFreq < (stableFreq + 0.001):
			contingency = 1

	if newFreq < (stableFreq):
		print "newFreq < stableFreq"
		if newFreq > (stableFreq - 1.0):
			contingency = -4
		if newFreq > (stableFreq - 0.1):
			contingency = -3
		if newFreq > (stableFreq - 0.01):
			contingency = -2
		if newFreq > (stableFreq - 0.001):
			contingency = -1
	contingency_plan(contingency)
	print "contingency: "
	print contingency

# Enables or disables devices
def contingency_plan(contingency):
	global nodeList
	print "in contingency_plan"
	print nodeList
	# For each mac address (appliance)


	for i in nodeList:
		if contingency < 0:
			if nodeList[i] < abs(contingency):
				# Disable everything in the appliance
				countp1 = i.split(',')[1] # get A=X
				countp2 = countp1.split('=')[1] # get X
				j = 0
				while j < int(countp2):
					publish.single("testbed/gateway/mqtt/" + i.split(',')[0], 'AO' + str(j) + '=0', hostname=BROKER_NAME)
					print 'AO' + str(j)
					j = j + 1
					time.sleep(1)
					# Need to wait due to limitation of the arduino

		if contingency > 0:
			if nodeList[i] < abs(contingency):
				# Disable everything in the appliance
				countp1 = i.split(',')[1] # get A=X
				countp2 = countp1.split('=')[1] # get X
				j = 0
				while j < int(countp2):
					publish.single("testbed/gateway/mqtt/" + i.split(',')[0], 'AO' + str(j) + '=1', hostname=BROKER_NAME)
					print 'AO' + str(j)
					j = j + 1
					time.sleep(1)
					# Need to wait due to limitation of the arduino


def freqThread():
	client = mqtt.Client()
	client.on_message = onUpdate_freq
	client.connect(BROKER_NAME, 1883)
	client.subscribe("testbed/scheduler/freq/#", 0)
	print "in freqThread"
	client.loop_forever()

# Continuously update node discover every 30 seconds
def sendND():
	try:
		while(True):
			publish.single("testbed/nodeDiscover/command/", 'START', hostname=BROKER_NAME)
			time.sleep(30)
	except:
		print "Publish ND command failed. Trying again in 30 seconds..."


def onUpdate_nodelist(mqttc, obj, msg):
	global nodeList
	print "in onUpdate_nodelist"
	nodes = msg.payload.split(" ")
	# print nodes
	for i in nodes:
		if "A=" in i:
			nodeList[(msg.topic.split('/')[3]) + ',' + i] = 1
			# print i

# Continuously receive new nodeDiscover data, and place it into nodeList.
def rcvND():
	client = mqtt.Client()
	client.on_message = onUpdate_nodelist
	client.connect(BROKER_NAME, 1883)
	client.subscribe("testbed/nodeDiscover/data/#", 0)
	client.loop_forever()


t1 = threading.Thread(target=freqThread)
t2 = threading.Thread(target=sendND)
t3 = threading.Thread(target=rcvND)
t1.start()
t2.start()
t3.start()