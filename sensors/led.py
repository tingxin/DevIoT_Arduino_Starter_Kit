__author__ = 'tingxxu'

import threading
import time

from DevIoTGateway.sensor import Sensor, SAction, SSetting
from DevIoTGateway.config import config
from DevIoTGatewayPi.sensorlogic import SensorLogic
from logic.arduinopioperator import ArduinopiOperator


led = Sensor("led", "led_2", "ALed")

on_action = SAction("on")
off_action = SAction("off")

flash_action = SAction("flash")

duration_setting = SSetting("duration", 0, [2, 100], 10, True)
interval_setting = SSetting("interval", 0, [0.1, 10], 1, True)
flash_action.add_setting(duration_setting)
flash_action.add_setting(interval_setting)

led.add_action(on_action)
led.add_action(off_action)
led.add_action(flash_action)


class LedLogic(SensorLogic):

    state = 0
    duration = 10
    interval = 1
    t = None

    @staticmethod
    def action(sensor, action):
        pin = config["sensors"][sensor.id]['pin']
        if action.name == 'on':
            LedLogic.do_on(pin)
        elif action.name == 'off':
            LedLogic.do_off(pin)
        elif action.name == 'flash':
            LedLogic.do_flash(action.parameters, pin)
        else:
            pass

    @staticmethod
    def write(data, pin):
        ArduinopiOperator.write(pin, data)

    @staticmethod
    def do_on(pin):
        LedLogic.write(1, pin)
        LedLogic.state = 1

    @staticmethod
    def do_off(pin):
        LedLogic.write(0, pin)
        LedLogic.state = 0

    @staticmethod
    def do_flash(parameters, pin):
        if parameters is not None:
            for parameter in parameters:
                if parameter.name == 'duration':
                    LedLogic.duration = int(parameter.value)
                elif parameter.name == 'interval':
                    LedLogic.interval = float(parameter.value)
                else:
                    pass

        if LedLogic.state == 2:
            return
        LedLogic.state = 2

        LedLogic.t = threading.Thread(target=LedLogic.flash, args=(pin, ))
        LedLogic.t.daemon = True
        LedLogic.t.start()

    @staticmethod
    def flash(pin):
        write_key = 0
        while (LedLogic.state == 2) and (LedLogic.duration > 0):
            LedLogic.write(write_key, pin)
            if write_key == 0:
                write_key = 1
            else:
                write_key = 0
            time.sleep(LedLogic.interval)
            LedLogic.duration -= LedLogic.interval
        if LedLogic.state == 2:
            LedLogic.write(0, pin)
            LedLogic.state = 0
        else:
            LedLogic.write(LedLogic.state, pin)
        # resume
        LedLogic.duration = 10
        LedLogic.interval = 1
