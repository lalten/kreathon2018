#! /usr/bin/python

import paho.mqtt.client as mqtt

import django
django.setup()
from backend.models import Measurement, Container

"""This class subscribes to a MQTT topic and receives measurements from the sensors. These values are then written
into the database"""


class MqttDBBridge():
    measurement_topic = "awesome_bin"   # Arduinos publish on this topic
    broker_url = "broker.mqttdashboard.com"  # url and port of public MQTT broker (no security...)
    broker_port = 1883

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MqttDBBridge.broker_url, MqttDBBridge.broker_port)

    def on_connect(self, client, userdata, flags, rc):
        assert isinstance(client, mqtt.Client)
        client.subscribe(MqttDBBridge.measurement_topic)

    def on_message(self, client, userdata, msg):
        if msg.topic == MqttDBBridge.measurement_topic:
            self._process_measurement(msg)
            return

        print ("Received msg on unhandled topic '%s'", msg.topic)

    @staticmethod
    def _process_measurement(msg):
        spl = msg.payload.split('_')
        if not len(spl) == 4:
            print("Received malformed message: %s" % msg.payload)
            return

        try:
            container_id, reading_msg, status, battery = map(int, spl)
        except ValueError:
            print("Received malformed message: %s" % msg.payload)
            return

        if status > 0:
            print "Not storing for invalid data: ", msg.payload
            return

        reading = reading_msg / 1000.0  # fixed comma

        try:
            container = Container.objects.get(id=container_id)
        except Container.DoesNotExist:
            print ("Invalid Container id: %i" % container_id)
            return

        container.reading_in_range(reading)

        m = Measurement(container=container, raw_reading=reading)
        m.save()
        print ("storing measurement: %s" % str(m))

    def spin(self):
        self.client.loop_forever()


if __name__ == "__main__":
    bridge = MqttDBBridge()
    bridge.spin()
