#! /usr/bin/python

import django
django.setup()

from backend.models import Container, Measurement

import flask
from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, request

app = Flask(__name__)
api = Api(app)


def get_container_info():

    msg = list()

    containers = Container.objects.all()
    print ("Number of containers: %i" % len(containers))
    for c in containers:
        measurements = Measurement.objects.filter(container_id=c.id)
        m_cnt = len(measurements)
        if m_cnt == 0:
            continue

        current = measurements.order_by('-id')[0]
        empty_val = c.reading_sonic_empty
        full_val = c.reading_sonic_full

        filling_level = (current.raw_reading-empty_val)/(full_val-empty_val)

        filling_level = min(filling_level, 1)
        filling_level = max(filling_level, 0)

        filling_level = 100-filling_level*100

        msg.append({'id': c.id, 'lng':c.lng, 'lat': c.lat,
                    'loc_str': c.location_string, 'level': filling_level, 'clean':3})
    return msg


@app.route('/containers', methods=['GET'])
def door_open():
    response = flask.jsonify({'containers': get_container_info()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# print get_container_info()
app.run(host='0.0.0.0')