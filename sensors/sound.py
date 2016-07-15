__author__ = 'tingxxu'

from DevIoTGateway.sensor import Sensor
from DevIoTGateway.sproperty import SProperty
from DevIoTGatewayPi.config import config
from DevIoTGatewayPi.sensorlogic import SensorLogic
from logic.arduinopioperator import ArduinopiOperator


sound = Sensor("sound", "sound_2", "ASound")

value_property = SProperty("volume", 0, [0, 100], 0)

sound.add_property(value_property)


class SoundLogic(SensorLogic):


    @staticmethod
    def update(sensor, data):
        pin = config["sensors"][sensor.id]['pin']
        new_value = ArduinopiOperator.read(pin)
        if new_value is not None:
            updated_properties = {"volume": new_value*100}
            SensorLogic.update_properties(sensor, updated_properties)