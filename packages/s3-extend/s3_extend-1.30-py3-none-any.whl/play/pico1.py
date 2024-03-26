#!/usr/bin/python
import array
from math import *
from struct import *

import serial


# Class definition / Interface for reading sensor values
class ScratchBoard:
    def __init__(self, serialPort):
        # The information received from the picoboard is packed in frames called channels,
        # each channel has a number so we associate them with names
        # ( more easy to be understood by humans :) )
        self.sbChannels = {0: "resistance-D", 1: "resistance-C",
                           2: "resistance-B", 3: "button", 4: "resistance-A",
                           5: "light", 6: "sound", 7: "slider", 15: "firmware-id"}
        # Everytime we request the values from the picoboard we have to
        # send first a byte with the following value b00000001
        self.pollToken = array.array('B', [1]).tobytes()
        # Store
        self.serialPort = serialPort
        self.ser = None

    def open(self):
        # Here we open a serial port using a rate of 38400 for
        # transfer and a timeout of 1 second. Also we flush everything that's on the line.
        self.ser = serial.Serial(self.serialPort, 38400, timeout=1)
        self.ser.read()
        self.ser.flushInput()

    def close(self):
        if self.ser is not None:
            self.ser.close()

    def getSensorValues(self):
        # Flush everything that is in the buffer... we need fresh data
        self.ser.flushInput()

        # Poll the scratch board (send 0x01 and receive a 18 bytes packet back)...
        # have a look at the packet structure in the printed documentation
        self.ser.write(self.pollToken)
        sbPacketString = self.ser.read(18)
        # sbPacket = unpack("BBBBBBBBBBBBBBBBBB", sbPacketString)
        sbPacket = sbPacketString

        # Parse the data received and extract useful info.. and store the
        # info into a hast-table (disctionary in python)
        result = {}
        for i in range(8):
            sb_channel = self.sbChannels[(int(sbPacket[2 * i]) - 128) >> 3]
            sb_value = ((int(sbPacket[2 * i]) & 7) << 7) + int(sbPacket[2 * i + 1])
            result[sb_channel] = sb_value

        # Adjust some the values to be more appropiate to be read by humans.
        # So for slider and button we have values between 0 and 100.
        for tmp in ["slider", "button"]:
            result[tmp] = int((100 * result[tmp]) / 1023)

        return result

    # make some adjustmets for the value received from the light sensor
    def light(self, value):
        if value < 25:
            return 100 - value
        return (1023 - value) * (75 / 998)

    # make some adjustmets for the value received from the sound sensor
    def sound(self, value):
        n = max(0, value - 18)
        if n < 50:
            return int(n / 2)
        return 25 + min(75, int((n - 50) * (75 / 580)))

    # return the value of the slider. a value between 0 and 100
    def getSliderValue(self):
        return self.getSensorValues()["slider"]

    # return the button value. 0=pressed, 100=unpressed
    def getButtonValue(self):
        return self.getSensorValues()["button"]

    # return raw information from the light sensor
    def getLightValue(self):
        return self.getSensorValues()["light"]

    # return raw information from the sound sensor
    def getSoundValue(self):
        return self.getSensorValues()["sound"]

    # return the value of the resistance measured on channel A. the result should be in kOhms
    def getResistanceAValue(self):
        x = self.getSensorValues()["resistance-A"]
        # TO DO: adjust x to be a measure of kOhms
        # ex: if you have x expressed in Ohms to make it be expressed in kOhms you have to write:
        #     x = x / 1000
        x = 0.9063 * exp(0.0468 * x / 1023. * 100.)
        return x

    def getResistanceBValue(self):
        x = self.getSensorValues()["resistance-B"]
        return x

    def getResistanceCValue(self):
        x = self.getSensorValues()["resistance-C"]
        return x

    def getResistanceDValue(self):
        x = self.getSensorValues()["resistance-D"]
        return x

#
# Simple usage example
#
# from pico import *        -> import the pico modules... make sure that
# the pico.py is in the same directory as your program
pico = ScratchBoard('/dev/ttyACM0')
pico.open()
# print "Button=",pico.getButtonValue()
print ("light=",pico.getLightValue())
pico.close()
#
