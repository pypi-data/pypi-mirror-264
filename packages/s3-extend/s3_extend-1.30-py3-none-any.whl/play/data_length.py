"""
 Copyright (c) 2019 Alan Yorinks All rights reserved.
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.
 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import serial
from serial.tools import list_ports
import sys
import threading
import time


class PBR:
    """
    Picoboard data reader. This program will normalize all analog values to be
    within a range of 0 - 100.
    It normalizes light values so that 0 is no light, and 100 is maximum.

    Normally, line feed carriage returns are suppressed in the output.
    Usage:
        python3 pbr.py

    To enable line feeds and carriage returns, start the program with a single
    value on the command line.
    Usage:
        python3 pbr.py x

    """

    def __init__(self, com_port=None):
        self.baud_rate = 38400

        self.count = 0
        self.picoboard = serial.Serial(sys.argv[1], self.baud_rate,
                                           timeout=.3, writeTimeout=0)

        print('serial port open...')
        # self.picoboard.reset_input_buffer()
        # self.picoboard.reset_output_buffer()
        character_count = 0
        self.data_stream = []
        time.sleep(1)
        for i in range(10):
            self.picoboard.write(b'\x01')
        # self.picoboard.write(b'\x01')

        # time.sleep(1)
        while True:
            if self.picoboard.inWaiting():
                c = self.picoboard.read()
                self.count += 1
                print(self.count)
                # self.command_deque.append(ord(c))
            else:
                time.sleep(.1)





PBR()
