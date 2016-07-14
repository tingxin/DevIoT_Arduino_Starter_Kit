__author__ = 'tingxxu'

import threading
import time

from DevIoTGateway.sensor import Sensor, SAction, SSetting
from DevIoTGatewayPi.config import config
from DevIoTGatewayPi.sensorlogic import SensorLogic
from logic.arduinopioperator import ArduinopiOperator


buzzer = Sensor("buzzer", "buzzer_2", "ABuzzer")

on_action = SAction("on")
off_action = SAction("off")


duration_setting = SSetting("duration", 0, [2, 100], 10, True)
interval_setting = SSetting("interval", 0, [0.1, 10], 1, True)
on_action.add_setting(duration_setting)
on_action.add_setting(interval_setting)

buzzer.add_action(on_action)
buzzer.add_action(off_action)


class BuzzerLogic(SensorLogic):

    state = 0
    duration = 10
    interval = 1
    t = None

    @staticmethod
    def action(sensor, action):
        pin = config["sensors"][sensor.id]['pin']
        if action.name == 'on':
            BuzzerLogic.do_on(action.parameters, pin)
        elif action.name == 'off':
            BuzzerLogic.do_off(pin)
        else:
            pass

    @staticmethod
    def write(data, pin):
        ArduinopiOperator.write(pin, data)
        
    @staticmethod
    def do_off(pin):
        BuzzerLogic.write(0, pin)
        BuzzerLogic.state = 0

    @staticmethod
    def do_on(parameters, pin):
        if parameters is not None:
            for parameter in parameters:
                if parameter.name == 'duration':
                    BuzzerLogic.duration = int(parameter.value)
                elif parameter.name == 'interval':
                    BuzzerLogic.interval = float(parameter.value)
                else:
                    pass

        if BuzzerLogic.state == 2:
            return
        BuzzerLogic.state = 2

        BuzzerLogic.t = threading.Thread(target=BuzzerLogic.flash, args=(pin,))
        BuzzerLogic.t.daemon = True
        BuzzerLogic.t.start()

    @staticmethod
    def flash(pin):
        write_key = 0
        while (BuzzerLogic.state == 2) and (BuzzerLogic.duration > 0):
            BuzzerLogic.write(write_key, pin)
            if write_key == 0:
                write_key = 1
            else:
                write_key = 0
            time.sleep(BuzzerLogic.interval)
            BuzzerLogic.duration -= BuzzerLogic.interval
        if BuzzerLogic.state == 2:
            BuzzerLogic.write(0, pin)
            BuzzerLogic.state = 0
        else:
            BuzzerLogic.write(BuzzerLogic.state, pin)
        # resume
        BuzzerLogic.duration = 10
        BuzzerLogic.interval = 1
