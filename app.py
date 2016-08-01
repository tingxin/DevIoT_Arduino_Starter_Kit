__author__ = 'tingxxu'

from DevIoTGateway.config import config
from DevIoTGatewayPi.pigateway import PiGateway
from logic.arduinopioperator import ArduinopiOperator
from logic.defaultsensorlogic import DefaultSensorLogic



if __name__ == '__main__':

    ArduinopiOperator.setup()

    devIot_address = config.get_string("address", "10.140.92.25:9000")
    mqtt_address = config.get_string("mqtthost", "10.140.92.25:1883")
    app_name = config.get_string("appname", "arduino")
    devIot_account = config.get_info("account", "")

    app = PiGateway(app_name, devIot_address, mqtt_address, devIot_account)
    app.default_sensor_logic = DefaultSensorLogic
    app.run()