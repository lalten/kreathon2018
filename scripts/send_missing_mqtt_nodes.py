#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import random
import time
import numpy as np
import paho.mqtt.client as mqtt


class SendMissingMqttNodes:
    measurement_topic = "awesome_bin"   # Arduinos publish on this topic
    broker_url = "broker.mqttdashboard.com"  # url and port of public MQTT broker (no security...)
    broker_port = 1883

    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(SendMissingMqttNodes.broker_url, SendMissingMqttNodes.broker_port)
        self.client.loop_start()
        self.fill_level = np.zeros((101, 1))

    def spin(self):
        try:
            while True:
                for sensor_id in range(5, 101):
                    self.fill_level[sensor_id] += 100 * random.random()
                    self.fill_level[sensor_id] = min(self.fill_level[sensor_id], 1000)
                    if self.fill_level[sensor_id] == 1000:
                        self.fill_level[sensor_id] = 0  # just reset to zero for now
                    range_status = 0
                    bat_mv = -1
                    this_fill_level = int(round(self.fill_level[sensor_id]))
                    payload_str = '{}_{}_{}_{}\n'.format(sensor_id, this_fill_level, range_status, bat_mv)
                    self.client.publish(SendMissingMqttNodes.measurement_topic, payload_str)
                time.sleep(1)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    n = SendMissingMqttNodes()
    n.spin()
