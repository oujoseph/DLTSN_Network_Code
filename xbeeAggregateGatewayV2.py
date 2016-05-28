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
import binascii
# -----------------------------------------------------------------------------
# Config Settings
PORT = '/dev/ttyUSB0'
BAUD = 19200
BROKER_NAME = "127.0.0.1"
# Config Settings
# -----------------------------------------------------------------------------

ser = serial.Serial(PORT, BAUD)
ser.timeout=10
xbee = XBee(ser)
ser.flushInput()
ser.flushOutput()

# xbee = XBee(object)

# Must be used with .encode('hex'); omitted in these functions for readability
def MACtoHex(response, param):
    return response[param][2:10]
def addrToHex(response, param):
    return response[param][0:2]

def rxData():
    print "in rxData"
    CONST_AT = 1
    CONST_DATA = 2
    CONST_STATUS = 3
    # loop forever and read the next frame
    while True:
        try:
            print "reading frame"
            # 3 types of possible frames: AT frames, data frames, and status frames
            frameType = 0
            status = xbee.wait_read_frame()
            print status
            if 'tx_status' in status:
                if 'status' in status:
                    if status['status'] == '\x00':
                        topicStruct = ('testbed/gateway/data/' + status['source_addr'].encode('hex'))
                        publish.single(topicStruct, "RECEIVED", hostname=BROKER_NAME)
                        frameType = CONST_STATUS

            if 'rf_data' in status:
                if 'rf_data' in status:
                    t=status['rf_data'].split('\r\n')[0]
                    # t=t.split('=')[1]
                    
                    # If the response is an ND command, pass it to node discover. else, pass it to testbed/gateway/data
                    if ":" in t:
                        print "ND IN T"
                        print t
                        t = t.split(':')[1]
                        print t
                        topicStruct = ('testbed/nodeDiscover/data/' + status['source_addr'].encode('hex'))
                        publish.single(topicStruct, t, hostname=BROKER_NAME)
                        frameType = CONST_DATA
                    else:
                        print "NO ND IN T"
                        topicStruct = ('testbed/gateway/data/' + status['source_addr'].encode('hex'))
                        publish.single(topicStruct, t, hostname=BROKER_NAME)
                        frameType = CONST_DATA


            if 'command' in status:
                print "command in status"
                if status['command'] == 'ND':

                    print "status['command'] == ND'"

                    # If a node has responded, parse the response to get the mac address
                    # Then, publish to that address inside testbed/gateway/nodes/
                    frameType = CONST_AT
                    if 'parameter' in status:
                        print 'parameter in status'
                        topicStruct = ('testbed/gateway/nodes/')
                        print topicStruct
                        print "publishing data"
                        publish.single(topicStruct, MACtoHex(status,'parameter').encode('hex'), hostname=BROKER_NAME)
                        print "published"
                    # Publish "END" if the last AT command response has been received
                    else:
                        topicStruct = ('testbed/gateway/nodes/')
                        publish.single(topicStruct, "END", hostname=BROKER_NAME)
        except:
            print "an error occured in rxData"


def on_message(mqttc, obj, msg):
    try:
        print "MQTT MESSAGE RECEIVED"
        # If the received message is a node discover command, send an AT command.
        # If not, it is a data message, and forward it to the xbee.
        if msg.payload == "NODE_DISCOVER":
            xbee.at(frame_id='1', command='ND')
        else:
            mac = msg.topic.split("/")[3]
            print "MAC ADDRESS IS:" + mac
            print binascii.unhexlify(mac)
            payload = msg.payload

            # If payload is not a properly formed command in hex,
            # convert to hex and make sure the result is terminated with a carriage return. 
            if "\x0A" not in payload:
                print "\\x found in payload. hexlifying: "
                conv = payload.encode("hex") + "0A"
                payload = binascii.unhexlify(conv)

            print "DATA SENT IS:" + payload
            payload = payload.split('\r')[0]
            print "SENDING AN XBEE FRAME"
            xbee.tx_long_addr(frame_id='2', dest_addr=binascii.unhexlify(mac), data=payload)
            print "SENT"
    except:
        print "An error occurred in on_message"

def txData():
    # for specific client:
    # mqttc = mqtt.Client("client-id")
    print "in txdata"
    mqttc = mqtt.Client("xbeeGateway")
    mqttc.on_message = on_message
    mqttc.connect(BROKER_NAME, 1883, 60)
    mqttc.subscribe("testbed/gateway/mqtt/#", 0)
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