__author__ = 'tingxxu'

from DevIoTGateway.sensor import Sensor
from DevIoTGateway.sproperty import SProperty
from DevIoTGatewayPi.config import config
from DevIoTGatewayPi.sensorlogic import SensorLogic
from logic.arduinopioperator import ArduinopiOperator


light = Sensor("light", "light_2", "ALight")

value_property = SProperty("value", 0, [0, 100], 0)

light.add_property(value_property)


class LightLogic(SensorLogic):

    @staticmethod
    def update(sensor, data):
        pin = config["sensors"][sensor.id]['pin']
        new_value = ArduinopiOperator.read(pin)*100
        updated_properties = {"value": new_value}
        SensorLogic.update_properties(sensor, updated_properties)
