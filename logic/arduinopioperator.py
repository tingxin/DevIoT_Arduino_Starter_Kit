__author__ = 'tingxxu'

from DevIoTGateway.config import config
from DevIoTGatewayPi.pioperator import PiOperator

from pyfirmata import Arduino, util


import os
import random


PORT = config["serialport"]

is_debug = False
if "DEBUG" in os.environ:
    is_debug = os.environ['DEBUG'] == 'TRUE'


class ArduinopiOperator(PiOperator):
    board = None
    report_cache = {}
    @staticmethod
    def setup():
        ArduinopiOperator.board = Arduino(PORT)
        it = util.Iterator(ArduinopiOperator.board)
        it.start()

        all_sensors = config["sensors"]

        for sensor_key in all_sensors:
            ArduinopiOperator.board.analog[all_sensors[sensor_key]["pin"]].enable_reporting()

    @staticmethod
    def write(pin, data):
        if is_debug is False:
            ArduinopiOperator.board.digital[pin].write(data)
        else:
            print("write data..." + str(data))

    @staticmethod
    def read(pin):
        if is_debug is False:
            return ArduinopiOperator.board.analog[pin].read()
        else:
            return random.randint(0, 100)
