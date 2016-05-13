#! /usr/bin/python
#  use carriage returns as a standard delimiter


from xbee import XBee
import serial
# from dummySerial import XBee
from datetime import datetime
from time import sleep
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading
from multiprocessing import Process

PORT = '/dev/ttyUSB0'
BAUD = 19200
BROKER_NAME = "127.0.0.1"


ser = serial.Serial(PORT, BAUD)
ser.timeout=10
xbee = XBee(ser)
ser.flushInput()
ser.flushOutput()

# xbee = XBee(object)

# RunningNodes is a dict that should be wiped after a few runs
# unique_ids never gets wiped and keeps track of all nodes that
# are and have been on the network since program start.
runningNodes = {}
unique_ids = {}

# parses the mac address in the 'parameter' element of a return
def MACtoHex(response, param):
    return response[param][2:10]
def addrToHex(response, param):
    return response[param][0:2]

def getND(xbee, runningNodes, uniqueDict):
    # frame_id has to be something; anything will work, we don't care
    # what it is. frame_id is just for bookkeeping.
    print "SENDING AT COMMAND"
    xbee.at(frame_id='1', command='ND')
    print "WAITING ON RESPONSE"
    response=xbee.wait_read_frame(timeout=1)
    # print "RECEIVED RESPONSE"
    # print response['parameter'].encode('hex')
    # print MACtoHex(response,'parameter').encode('hex')
    #initialize response for for loop
    if 'command' in response:
        print "[[IN COMMAND RESPONSE]]"
        # if command is 'ND', check if it has a parameter.
        # if it does, it is a response from a client.
        # if it doesn't, all clients have been found.
        if response['command'] == 'ND':
            if 'parameter' in response:
                # runningNodes[c] = addrToHex(response, 'parameter')
                #If a new node is found
                if addrToHex(response, 'parameter') not in uniqueDict:
                    runningNodes[addrToHex(response, 'parameter')] = MACtoHex(response, 'parameter')
                    uniqueDict[addrToHex(response, 'parameter')] = MACtoHex(response, 'parameter')
                #if adding a node already in the network, add it to runningNodes.
                #if trying to add a node to an address occupied by something else
                #change the address of the node.
                #TODO: when we start using 64bit addresses, don't need to worry about this
                elif uniqueDict[addrToHex(response, 'parameter')] == MACtoHex(response, 'parameter'):
                    runningNodes[addrToHex(response, 'parameter')] = MACtoHex(response, 'parameter')
                    # else uniqueDict
    else:
        return
    while True:
        # checks if 'command' is found. if not found
        # and haven't yet broken from program, keep scanning
        if 'command' in response:
            # if command is 'ND', check if it has a parameter.
            # if it does, it is a response from a client.
            # if it doesn't, all clients have been found.
            if response['command'] == 'ND':
                if 'parameter' in response:
                    # TODO: need to check to see if two clients have the same address.
                    runningNodes[addrToHex(response, 'parameter')] = MACtoHex(response, 'parameter')
                    uniqueDict[addrToHex(response, 'parameter')] = MACtoHex(response, 'parameter')
                    response = xbee.wait_read_frame(timeout=1)
                    # print MACtoHex(response, 'parameter')
                else:
                    break
            else:
                break
        else: 
            response = xbee.wait_read_frame(timeout=1)


def iterateNodes(xbee, runningNodes, uniqueDict):
    # while True:
    print "in iterator nodes"
    for key in runningNodes:
        # InfoIdConv just sets the info_id as the destination address
        status = None
        t = 9999
        #defaults to temperature sensor

        try:
            xbee.tx(frame_id='2', dest_addr=key, data='\x54\x3F\x0A')
            # xbee.tx(frame_id='2', dest_addr=key, data='\x4C\x3F\x0A')
            print '[WAITING ON DATA]'
            status=xbee.wait_read_frame(timeout=1)
            # if status['sdz']:
            #     print "hi"
            print status
            print 'RECEIVED DATA]'
            status=xbee.wait_read_frame(timeout=1)
            print status
            t=status['rf_data'].split('/r/n')[0]
            t=t.split('\n')[0]
            t=t.split('=')[1]
            print 'RECEIVED RF DATA: ' + t
            mqttUploadString = ('testbed/' + key.encode('hex'))
            print "Sending message to broker on topic: " + mqttUploadString
            publish.single(mqttUploadString, t, hostname=BROKER_NAME)
        except:
            print "EXCEPTION IN ITERATE NODES"

def rxData():
    while True:
        getND(xbee, runningNodes, unique_ids)
        iterateNodes(xbee, runningNodes, unique_ids)
        # clear runningNodes after an iteration.
        runningNodes.clear()
        # print sorted(unique_ids.values())
        # print sorted(unique_ids.key())

def on_message(mqttc, obj, msg):
    print "MQTT MESSAGE RECEIVED"

    print "SENDING AN XBEE FRAME"
    xbee.tx(frame_id='2', dest_addr='\x00\x02', data='\x54\x3F\x0A')
    print "SENT"
def txData():
    # for specific client:
    # mqttc = mqtt.Client("client-id")
    print "in txdata"
    mqttc = mqtt.Client("GatewayRx")
    mqttc.on_message = on_message
    mqttc.connect(BROKER_NAME, 1883, 60)
    mqttc.subscribe("test", 0)
    mqttc.loop_forever()



# 2 threads:
# rxData has 2 purposes: compile a list of all connected nodes, and pass received data to broker
# txData transmits commands sent by a client.
try:
    txThread = threading.Thread(target=txData)
    rxThread = threading.Thread(target=rxData)
    rxThread.start()
    txThread.start()
    
except:
    print "Problem starting a new thread"