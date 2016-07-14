__author__ = 'tingxxu'

from DevIoTGatewayPi.config import config
from DevIoTGatewayPi.sensorlogic import SensorLogic
from arduinopioperator import ArduinopiOperator


class DefaultSensorLogic(SensorLogic):

    @staticmethod
    def update(sensor, data):
        pin = config["sensors"][sensor.id]['pin']
        new_value = ArduinopiOperator.read(pin)
        updated_properties = {"value": new_value}
        SensorLogic.update_properties(sensor, updated_properties)

    @staticmethod
    def action(sensor, action):
        pin = config["sensors"][sensor.id]['pin']
        if action.name == 'on':
            ArduinopiOperator.write(pin, 1)
        elif action.name == 'off':
            ArduinopiOperator.write(pin, 0)
        else:
            pass