__author__ = 'tingxxu'

import math

from DevIoTGateway.sensor import Sensor
from DevIoTGateway.sproperty import SProperty
from DevIoTGateway.config import config
from DevIoTGatewayPi.sensorlogic import SensorLogic
from logic.arduinopioperator import ArduinopiOperator


temperature = Sensor("temperature", "temperature_2", "AThermometer")

value_property = SProperty("value", 0, [0, 100], 0)
value_property.unit = "Celsius"
temperature.add_property(value_property)


class TemperatureLogic(SensorLogic):

    @staticmethod
    def update(sensor, data):
        pin = config["sensors"][sensor.id]['pin']
        raw_value = ArduinopiOperator.read(pin)
        if raw_value is not None:
            new_value = 0
            if raw_value != 0:
                b_key = 4250
                resistance = (1023 - raw_value) * 10000.0 / raw_value
                new_value = 1/(math.log(resistance/10000)/b_key+1/298.15)-273.15 + 100
            updated_properties = {"value": new_value}
            sensor.update_properties(updated_properties)
