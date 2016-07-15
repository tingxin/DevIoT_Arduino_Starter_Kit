__author__ = 'tingxxu'

from DevIoTGateway.sensor import Sensor, SProperty
from DevIoTGatewayPi.sensorlogic import SensorLogic
from DevIoTGatewayPi.config import config
from logic.arduinopioperator import ArduinopiOperator

button = Sensor("button", "button_a", "AButton")

value_property = SProperty("pressed", 0, None, 0)

button.add_property(value_property)


class ButtonLogic(SensorLogic):

    @staticmethod
    def update(sensor, data):
        pin = config["sensors"][sensor.id]['pin']
        new_value = ArduinopiOperator.read(pin)
        if new_value is not None:
            if new_value == 0:
                updated_properties = {"pressed": 0}
            else:
                updated_properties = {"pressed": 1}
            SensorLogic.update_properties(sensor, updated_properties)
