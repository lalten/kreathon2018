#! /usr/bin/python


""" This File contains the Backend. The program offers different REST-API-Endpoints so that the webserver and the
telegram App can read and send data from and to the Database. The database (a sqlite-db) is attached using Django.

The Following interfaces are available:
/get_best:
    Expects a position in the latitude/longitude foremat (in 'lat', 'lng') and returns the closest Container that is
    not full. This is used by the chatbot when the user asks for the closest Container

/get_closest:
    Similar to get_best but returns the closest Container even though it is full. This function is used when the user
    wants to give a feedback about the cleanliness and should of course have the possibility to rate a full Container.

/containers:
    Returns a list of all Containers with their pose, (gps and human readable), their fill level and cleanliness

/feedback:
    Interface to write a users feedback about the cleanliness of a container into the database.

"""

import django
django.setup()
from geopy.distance import distance

from backend.models import Container, Measurement, Feedback, User
from copy import deepcopy
import flask
from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, request

app = Flask(__name__)
api = Api(app)

from sequence_optimization import calc_route


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

        filling_level = filling_level*100

        # get last Feedback for this container
        feedbacks = Feedback.objects.filter(container_id=c.id)
        f_cnt = len(feedbacks)
        clean = -1
        if f_cnt > 0:
            last_feedback = feedbacks.order_by('-id')[0]
            clean = last_feedback.rating

        msg.append({'id': c.id, 'lng': c.lng, 'lat': c.lat,
                    'loc_str': c.location_string, 'level': filling_level, 'clean': clean})
    return msg


@app.route('/get_best', methods=['POST'])
def get_best_container():
    d = request.form
    # lat = d['lat']
    # lng = d['lng']

    u_pos_tp = (float(d['lat']), float(d['lng']))
    u_pos = "%f,%f" % (float(d['lat']), float(d['lng']))

    min_dist = -1
    closest_container_id= -1
    best_pos = ""

    container_info = get_container_info()
    for c in container_info:

        if c['level'] > 90:
            print ("%i full" % c['id'])
            continue

        c_pos = "%f,%f" % (c['lat'], c['lng'])

        # check direct distance to see if we have to run the route planning
        d_direct = distance(u_pos_tp, (c['lat'], c['lng'])).m
        if d_direct > min_dist > 0:
            continue

        route = calc_route([u_pos, c_pos], 'pedestrian')
        d_sum = 0
        for m in route['response']['route'][0]['leg'][0]['maneuver']:  # single leg
            d_sum += m['length']

        if min_dist < 0 or d_sum < min_dist:
            min_dist = d_sum
            closest_container_id = deepcopy(c['id'])
            best_pos = c_pos

    answer = dict()
    answer['dist'] = d_sum
    answer['closest_container_id'] = closest_container_id
    answer['closest_container_pos'] = best_pos
    answer['location_string'] = Container.objects.get(id=closest_container_id).location_string

    response = flask.jsonify({'best_container': answer})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_closest', methods=['POST'])
def get_closest_container():
    d = request.form
    # user, created = User.objects.get_or_create(id=d['user_id'])
    # user.first_name = d['first_name']
    # user.save()

    # print user, created
    lat, lng = d['lat'], d['lng']

    feedback_pos = (lat, lng)
    best_pos = feedback_pos

    # get closest container:
    containers = Container.objects.all()
    print (len(containers))
    min_dist = -1
    closest_container_id = -1
    for c in containers:
        container_pos = (c.lat, c.lng)
        dist = distance(feedback_pos, container_pos).m
        # print "meters", dist

        # d = pow(lat-c.lat, 2) + pow(lng-c.lng, 2)
        if min_dist < 0 or dist < min_dist:
            min_dist = dist
            closest_container_id = c.id
            best_pos = [c.lat, c.lng]

    answer = dict()
    answer['dist'] = min_dist
    answer['closest_container_id'] = closest_container_id
    answer['closest_container_pos'] = best_pos
    answer['location_string'] = Container.objects.get(id=closest_container_id).location_string

    response = flask.jsonify({'closest_container': answer})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/containers', methods=['GET'])
def send_container():
    response = flask.jsonify({'containers': get_container_info()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/feedback', methods=['POST'])
def store_feedback():
    d = request.form
    user, created = User.objects.get_or_create(id=d['user_id'])
    user.first_name = d['first_name']
    user.save()

    c = Container.objects.get(id=d['container_id'])
    f = Feedback(user=user, lat=c.lat, lng=c.lng, container_id=c.id, rating=d['clean'])
    f.save()

    response = flask.jsonify(dict())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# print get_container_info()
app.run(host='0.0.0.0')