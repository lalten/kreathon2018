#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import time
import paho.mqtt.client as mqtt


class SendMissingMqttNodes:
    measurement_topic = "awesome_bin"   # Arduinos publish on this topic
    broker_url = "broker.mqttdashboard.com"  # url and port of public MQTT broker (no security...)
    broker_port = 1883

    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(SendMissingMqttNodes.broker_url, SendMissingMqttNodes.broker_port)
        self.client.loop_start()

    def spin(self):
        try:
            while True:
                for sensor_id in range(5, 101):
                    fill_level = 0
                    range_status = 0
                    bat_mv = -1
                    payload_str = '{}_{}_{}_{}\n'.format(sensor_id, fill_level, range_status, bat_mv)
                    self.client.publish(SendMissingMqttNodes.measurement_topic, payload_str)
                time.sleep(5)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    n = SendMissingMqttNodes()
    n.spin()
