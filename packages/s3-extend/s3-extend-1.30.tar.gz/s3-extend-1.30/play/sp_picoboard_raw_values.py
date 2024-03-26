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
import time


class SpPicoBoardReader:
    """
    Read the raw values from a picoboard
    """

    def __init__(self, com_port=None):
        self.baud_rate = 38400

        the_ports_list = list_ports.comports()
        for port in the_ports_list:
            print(f'Board Info: manufacturer: {port.manufacturer}, hwid: {port.hwid}')

        self.channels = {0: "D", 1: "C",
                         2: "B", 3: "btn", 4: "A",
                         5: "lt", 6: "snd", 7: "slide", 15: "id"}

        self.data_packet = None
        if com_port:
            self.picoboard = serial.Serial(com_port, self.baud_rate,
                                           timeout=1, writeTimeout=0)
        else:
            # self.find_the_picoboard()
            # print('picoboard found on:', self.picoboard.port)
            print('You must specify the com port')

        poll_picoboard = b'\x01'

        while True:

            self.picoboard.write(poll_picoboard)
            # allow some time for bidirectional data transfer
            try:
                time.sleep(.005)
            except KeyboardInterrupt:
                print('Control C detected')
                self.picoboard.close()
                sys.exit(0)

            # clear local variables in anticipation of the data
            self.data_packet = None
            sb_channel = None
            sb_value = None
            s_result = ''

            # if there is data available, then there should be
            # 18 bytes
            if self.picoboard.inWaiting():
                try:
                    self.data_packet = self.picoboard.read(18)
                except KeyboardInterrupt:
                    print('Control C detected')
                    self.picoboard.close()
                    sys.exit(0)

                # for each of the channels
                for i in range(9):
                    try:
                        sb_channel = self.channels[(int(self.data_packet[2 * i]) - 128) >> 3]
                        sb_value = ((int(self.data_packet[2 * i]) & 7) << 7) + int(self.data_packet[2 * i + 1])
                    except (KeyError, IndexError):
                        print(f'i = {i}, sb_channel = {sb_channel}, sb_value = {sb_value}')
                        raise

                    s_result = s_result + sb_channel + '=' + str(sb_value) + ' '

                # continuous printout on a single line
                # if you want multiple line output, comment this line
                # out and uncomment the next line
                print('\r' + s_result, end=' ')

                # print(s_result)


# SpPicoBoardReader('/dev/cu.usbserial-A40138PS')

SpPicoBoardReader('/dev/ttyACM0')
