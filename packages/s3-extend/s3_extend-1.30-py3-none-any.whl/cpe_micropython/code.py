from digitalio import DigitalInOut, Direction, Pull
import board
from adafruit_circuitplayground.express import cpx
import time
import sys


class CPX:
    def __init__(self):

        # a look up table for executing incoming commands
        cmd_dict = {'v': self.version,
                    'do': self.digital_out,
                    'di': self.digital_in,
                    'pwm': self.pwm,
                    'sonar': self.sonar,
                    'servo': self.servo,
                    'btna': self.read_button_a,
                    'btnb': self.read_button_b,
                    'sw': self.read_switch,
                    'tp': self.tapped,
                    'temp': self.temperature,
                    'lt': self.light,
                    'px': self.pixels,
                    'acc': self.accel,
                    'touch': self.touch,
                    'tone': self.tone,
                    }

        # a map of pin names to actual pin objects
        self.pin_map = {'a0': {'pin': board.A0, 'pin_obj': None},
                        'a1': {'pin': board.A1, 'pin_obj': None},
                        'a2': {'pin': board.A2, 'pin_obj': None},
                        'a3': {'pin': board.A3, 'pin_obj': None},
                        'a4': {'pin': board.A4, 'pin_obj': None},
                        'a5': {'pin': board.A5, 'pin_obj': None},
                        'a6': {'pin': board.A6, 'pin_obj': None},
                        }

        while True:
            while True:
                cmd_in = sys.stdin.readline().strip()
                cmd_in = cmd_in.split(',')

                if cmd_in[0] in cmd_dict:
                    cmd_dict[cmd_in[0]](cmd_in)

    def version(self, args):
        """
        print the software version number
        """
        print('CPEX-1.0')

    def digital_in(self, args):
        if args[1] in self.pin_map:
            pin = self.pin_map[args[1]]
            if not pin['pin_obj']:
                working_pin = DigitalInOut(pin['pin'])
                working_pin.direction = Direction.INPUT
                if args[2] == '1':
                        working_pin.pull = Pull.UP
                elif args[2] == '2':
                    working_pin.pull = Pull.DOWN
                pin['pin_obj'] = working_pin
            else:
                working_pin = pin['pin_obj']

            if working_pin.direction == Direction.INPUT:
                print(int(working_pin.value))


    def pwm(self, args):
        print('not yet')

    def sonar(self, args):
        print('not yet')

    def servo(self, args):
        print('not_yet')

    def digital_out(self, args):
        if args[1] != 'led':
            if args[1] in self.pin_map:
                pin = self.pin_map[args[1]]
                if not pin['pin_obj']:
                    working_pin = DigitalInOut(pin['pin'])
                    working_pin.direction = Direction.OUTPUT
                    pin['pin_obj'] = working_pin
                else:
                    working_pin = pin['pin_obj']

                if working_pin.direction == Direction.OUTPUT:
                    working_pin.value = int(args[2])
                else:
                    print('TBD: send a message back')
        else:
            cpx.red_led = int(args[2])

    def read_button_a(self, args):
        if cpx.button_a:
            print('1')
        else:
            print('0')

    def read_button_b(self, args):
        if cpx.button_b:
            print('1')
        else:
            print('0')

    def read_switch(self, args):
        if cpx.switch:
            print('1')
        else:
            print('0')

    def tapped(self, args):

        cpx.detect_taps = 1

        print(int(cpx.tapped))

    def temperature(self, args):
        print(cpx.temperature)

    def light(self, args):
        print(cpx.light)

    def pixels(self, args):
        color = (int(args[1]),
                 int(args[2]),
                 int(args[3])
                 )

        if args[0] == '10':
            cpx.pixels.fill(color)

        else:
            cpx.pixels[int(args[0])] = color

    def accel(self, args):
        print(cpx.acceleration)

    def touch(self, args):
        if args[1] == '1':
            print(int(cpx.touch_A1))
        elif args[1] == '2':
            print(int(cpx.touch_A2))
        elif args[1] == '3':
            print(int(cpx.touch_A3))
        elif args[1] == '4':
            print(int(cpx.touch_A4))
        elif args[1] == '5':
            print(int(cpx.touch_A5))
        elif args[1] == '6':
            print(int(cpx.touch_A6))
        elif args[1] == '7':
            print(int(cpx.touch_A7))

    def tone(self, args):
        cpx.play_tone(int(args[1]), float(args[2]))




CPX()
