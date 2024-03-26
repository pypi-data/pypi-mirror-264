import sys
import time
from python_banyan.banyan_base import BanyanBase

class DigitalInput(BanyanBase):
    def __init__(self):
        super(DigitalInput, self).__init__(process_name='banyan_base')

    def send_set_digital_input_pin(self):
        topic = 'to_arduino_gateway'
        payload = {'command': 'set_mode_digital_input', 'pin': 13}
        self.publish_payload(payload, topic)

di = DigitalInput()
time.sleep(1)
di.send_set_digital_input_pin()
