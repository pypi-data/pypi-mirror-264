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


class PBoardData:
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

        self.data_packet = None
        if com_port:
            self.picoboard = serial.Serial(com_port, self.baud_rate,
                                           timeout=1, writeTimeout=0)
        else:
            self.find_the_picoboard()
            print('picoboard found on:', self.picoboard.port)
            self.picoboard.reset_input_buffer()
            self.picoboard.reset_output_buffer()

        self.result =''
        self.num_bytes = None

        threading.Thread.__init__(self)
        self.daemon = True
        self.stop_event = threading.Event()
        self.start()
        time.sleep(.2)
        x = b'\x01'

        while True:
            try:
                time.sleep(.1)
                self.picoboard.write(x)
            except KeyboardInterrupt:
                self.picoboard.close()
                sys.exit(0)

    def find_the_picoboard(self):
        # go through the ports looking for an active board

        the_ports_list = list_ports.comports()
        for port in the_ports_list:
            if port.pid is None:
                continue
            else:
                print('Looking for picoboard on: ', port.device)
                self.picoboard = serial.Serial(port.device, self.baud_rate,
                                               timeout=1, writeTimeout=0)
                time.sleep(2)
                while True:
                    self.picoboard.write(b'\x01')
                    time.sleep(1)
                    self.num_bytes = self.picoboard.inWaiting()
                    # print(num_bytes)

                    self.result = str(self.num_bytes) + '  '
                    self.data_packet = self.picoboard.read(self.num_bytes)


                    for i in range(self.num_bytes // 2):
                        sb_value = ((int(self.data_packet[2 * i]) & 7) << 7) + int(self.data_packet[2 * i + 1])
                        self.result += str(i) + ':' + str(sb_value) + ' '
                        # print(sb_channel)
                        # print(sb_value)

                    print(self.result)
                    self.picoboard.reset_input_buffer()
                    self.picoboard.reset_output_buffer()

PBoardData()
