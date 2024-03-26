"""
This program will scan for active serial
ports on the computer and print the port
and hwid for any port found.

To use:
    python3 sscan.py
"""

from serial.tools import list_ports

the_ports_list = list_ports.comports()
for port in the_ports_list:
    if port.pid is None:
        continue
    else:
        print('Port Found: ', port.device, port.hwid)
