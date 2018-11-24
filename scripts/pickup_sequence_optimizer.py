#! /usr/bin/python
# coding: utf8

from here_connector import *
from sequence_optimization import *
import json

import requests
pick_up_url = "https://wse.api.here.com/2/findpickups.json"

start_point = {'lat' : 51.33, 'lng': 6.54436}


def pickup_optimizer():
    # positions = get_positions(monday_route)
    container_response = requests.get('http://10.13.144.90:5000/containers', dict())
    all_containers = container_response.json()['containers']
    monday_containers = list()

    base_url = pick_up_url+"?app_id=%s&app_code=%s" % (app_id, app_code)
    base_url += "&mode=shortest;truck;traffic:disabled&improveFor=time"
    base_url += "&start=start_wp;%f,%f" % (start_point['lat'], start_point['lng'])
    base_url += "&end=end_wp;%f,%f" % (start_point['lat'], start_point['lng'])
    base_url += "&capacity=" + str(100)
    base_url += "&driverCost=" + str(1)
    base_url += "&vehicleCost=" + str(1)


    dest_counter = -1

    # drop_cmd = "&destination:%s;%f,%f;" % ("last_wp", start_point['lat'], start_point['lng'])

    non_empty_containers = list()
    for c in all_containers:
        if c['level'] > 30:
            non_empty_containers.append(c)

    print len(non_empty_containers)

    sorted_containers = sorted(non_empty_containers, key=lambda c: -c['level'])

    print sorted_containers


    for c in sorted_containers:
        # if c['id'] in monday_route:
            # print c['id']
            # monday_containers.append(c)

            dest_counter += 1

            id = 'waypoint' + str(2*dest_counter)
            load_name = 'job_' + str(2*dest_counter)
            value = int(c['level']) # je voller, desto value
            # capacity does not work!

            from_ = "%s;%f,%f;pickup:%s" % (id, c['lat'], c['lng'], load_name)
            to_ = "%s;%f,%f;drop:%s,value:%i" % ('waypoint' + str(2*dest_counter+1), start_point['lat'], start_point['lng'], load_name, value)

            base_url += "&destination" + str(2 * dest_counter) + '=' + from_
            base_url += "&destination" + str(2 * dest_counter + 1) + '=' + to_

            if dest_counter == 11:
                break

    print base_url
    resp = json.loads(requests.get(base_url).text)#['results']
    print resp
    # print

    print len(monday_route)

    for wp in resp['results'][0]['waypoints']:
        print wp['lat'], wp['lng']



resp = {u'errors': [], u'warnings': None, u'results': [{u'distance': u'20804', u'description': u'Targeted best solution: suboptimal; without traffic', u'interconnections': [{u'distance': 204.0, u'rest': 0.0, u'toWaypoint': u'waypoint0', u'fromWaypoint': u'start_wp', u'waiting': 0.0, u'time': 37.0}, {u'distance': 1045.0, u'rest': 0.0, u'toWaypoint': u'waypoint12', u'fromWaypoint': u'waypoint0', u'waiting': 0.0, u'time': 239.0}, {u'distance': 2354.0, u'rest': 0.0, u'toWaypoint': u'waypoint10', u'fromWaypoint': u'waypoint12', u'waiting': 0.0, u'time': 605.0}, {u'distance': 2503.0, u'rest': 0.0, u'toWaypoint': u'waypoint8', u'fromWaypoint': u'waypoint10', u'waiting': 0.0, u'time': 549.0}, {u'distance': 1915.0, u'rest': 0.0, u'toWaypoint': u'waypoint16', u'fromWaypoint': u'waypoint8', u'waiting': 0.0, u'time': 614.0}, {u'distance': 2372.0, u'rest': 0.0, u'toWaypoint': u'waypoint2', u'fromWaypoint': u'waypoint16', u'waiting': 0.0, u'time': 693.0}, {u'distance': 2906.0, u'rest': 0.0, u'toWaypoint': u'waypoint4', u'fromWaypoint': u'waypoint2', u'waiting': 0.0, u'time': 792.0}, {u'distance': 3649.0, u'rest': 0.0, u'toWaypoint': u'waypoint6', u'fromWaypoint': u'waypoint4', u'waiting': 0.0, u'time': 970.0}, {u'distance': 716.0, u'rest': 0.0, u'toWaypoint': u'waypoint14', u'fromWaypoint': u'waypoint6', u'waiting': 0.0, u'time': 297.0}, {u'distance': 2366.0, u'rest': 0.0, u'toWaypoint': u'waypoint13', u'fromWaypoint': u'waypoint14', u'waiting': 0.0, u'time': 627.0}, {u'distance': 86.0, u'rest': 0.0, u'toWaypoint': u'waypoint7', u'fromWaypoint': u'waypoint13', u'waiting': 0.0, u'time': 6.0}, {u'distance': 86.0, u'rest': 0.0, u'toWaypoint': u'waypoint3', u'fromWaypoint': u'waypoint7', u'waiting': 0.0, u'time': 6.0}, {u'distance': 86.0, u'rest': 0.0, u'toWaypoint': u'waypoint5', u'fromWaypoint': u'waypoint3', u'waiting': 0.0, u'time': 6.0}, {u'distance': 86.0, u'rest': 0.0, u'toWaypoint': u'waypoint1', u'fromWaypoint': u'waypoint5', u'waiting': 0.0, u'time': 6.0}, {u'distance': 86.0, u'rest': 0.0, u'toWaypoint': u'waypoint11', u'fromWaypoint': u'waypoint1', u'waiting': 0.0, u'time': 6.0}, {u'distance': 86.0, u'rest': 0.0, u'toWaypoint': u'waypoint17', u'fromWaypoint': u'waypoint11', u'waiting': 0.0, u'time': 6.0}, {u'distance': 86.0, u'rest': 0.0, u'toWaypoint': u'waypoint9', u'fromWaypoint': u'waypoint17', u'waiting': 0.0, u'time': 6.0}, {u'distance': 86.0, u'rest': 0.0, u'toWaypoint': u'waypoint15', u'fromWaypoint': u'waypoint9', u'waiting': 0.0, u'time': 6.0}, {u'distance': 86.0, u'rest': 0.0, u'toWaypoint': u'end_wp', u'fromWaypoint': u'waypoint15', u'waiting': 0.0, u'time': 6.0}], u'waypoints': [{u'sequence': 0, u'estimatedDeparture': u'2018-11-24T09:53:46Z', u'lat': 51.33, u'estimatedArrival': None, u'lng': 6.54436, u'id': u'start_wp', u'fulfilledConstraints': []}, {u'sequence': 1, u'estimatedDeparture': u'2018-11-24T09:54:23Z', u'lat': 51.330259, u'estimatedArrival': u'2018-11-24T09:54:23Z', u'lng': 6.545865, u'id': u'waypoint0', u'fulfilledConstraints': []}, {u'sequence': 2, u'estimatedDeparture': u'2018-11-24T09:58:22Z', u'lat': 51.32996, u'estimatedArrival': u'2018-11-24T09:58:22Z', u'lng': 6.53694, u'id': u'waypoint12', u'fulfilledConstraints': []}, {u'sequence': 3, u'estimatedDeparture': u'2018-11-24T10:08:27Z', u'lat': 51.32108, u'estimatedArrival': u'2018-11-24T10:08:27Z', u'lng': 6.52785, u'id': u'waypoint10', u'fulfilledConstraints': []}, {u'sequence': 4, u'estimatedDeparture': u'2018-11-24T10:17:36Z', u'lat': 51.32097, u'estimatedArrival': u'2018-11-24T10:17:36Z', u'lng': 6.54654, u'id': u'waypoint8', u'fulfilledConstraints': []}, {u'sequence': 5, u'estimatedDeparture': u'2018-11-24T10:27:50Z', u'lat': 51.325859, u'estimatedArrival': u'2018-11-24T10:27:50Z', u'lng': 6.55778, u'id': u'waypoint16', u'fulfilledConstraints': []}, {u'sequence': 6, u'estimatedDeparture': u'2018-11-24T10:39:23Z', u'lat': 51.322891, u'estimatedArrival': u'2018-11-24T10:39:23Z', u'lng': 6.5807, u'id': u'waypoint2', u'fulfilledConstraints': []}, {u'sequence': 7, u'estimatedDeparture': u'2018-11-24T10:52:35Z', u'lat': 51.3083, u'estimatedArrival': u'2018-11-24T10:52:35Z', u'lng': 6.56579, u'id': u'waypoint4', u'fulfilledConstraints': []}, {u'sequence': 8, u'estimatedDeparture': u'2018-11-24T11:08:45Z', u'lat': 51.33022, u'estimatedArrival': u'2018-11-24T11:08:45Z', u'lng': 6.565961, u'id': u'waypoint6', u'fulfilledConstraints': []}, {u'sequence': 9, u'estimatedDeparture': u'2018-11-24T11:13:42Z', u'lat': 51.33345, u'estimatedArrival': u'2018-11-24T11:13:42Z', u'lng': 6.572, u'id': u'waypoint14', u'fulfilledConstraints': []}, {u'sequence': 10, u'estimatedDeparture': u'2018-11-24T11:24:09Z', u'lat': 51.33, u'estimatedArrival': u'2018-11-24T11:24:09Z', u'lng': 6.54436, u'id': u'waypoint13', u'fulfilledConstraints': []}, {u'sequence': 11, u'estimatedDeparture': u'2018-11-24T11:24:15Z', u'lat': 51.33, u'estimatedArrival': u'2018-11-24T11:24:15Z', u'lng': 6.54436, u'id': u'waypoint7', u'fulfilledConstraints': []}, {u'sequence': 12, u'estimatedDeparture': u'2018-11-24T11:24:21Z', u'lat': 51.33, u'estimatedArrival': u'2018-11-24T11:24:21Z', u'lng': 6.54436, u'id': u'waypoint3', u'fulfilledConstraints': []}, {u'sequence': 13, u'estimatedDeparture': u'2018-11-24T11:24:27Z', u'lat': 51.33, u'estimatedArrival': u'2018-11-24T11:24:27Z', u'lng': 6.54436, u'id': u'waypoint5', u'fulfilledConstraints': []}, {u'sequence': 14, u'estimatedDeparture': u'2018-11-24T11:24:33Z', u'lat': 51.33, u'estimatedArrival': u'2018-11-24T11:24:33Z', u'lng': 6.54436, u'id': u'waypoint1', u'fulfilledConstraints': []}, {u'sequence': 15, u'estimatedDeparture': u'2018-11-24T11:24:39Z', u'lat': 51.33, u'estimatedArrival': u'2018-11-24T11:24:39Z', u'lng': 6.54436, u'id': u'waypoint11', u'fulfilledConstraints': []}, {u'sequence': 16, u'estimatedDeparture': u'2018-11-24T11:24:45Z', u'lat': 51.33, u'estimatedArrival': u'2018-11-24T11:24:45Z', u'lng': 6.54436, u'id': u'waypoint17', u'fulfilledConstraints': []}, {u'sequence': 17, u'estimatedDeparture': u'2018-11-24T11:24:51Z', u'lat': 51.33, u'estimatedArrival': u'2018-11-24T11:24:51Z', u'lng': 6.54436, u'id': u'waypoint9', u'fulfilledConstraints': []}, {u'sequence': 18, u'estimatedDeparture': u'2018-11-24T11:24:57Z', u'lat': 51.33, u'estimatedArrival': u'2018-11-24T11:24:57Z', u'lng': 6.54436, u'id': u'waypoint15', u'fulfilledConstraints': []}, {u'sequence': 19, u'estimatedDeparture': None, u'lat': 51.33, u'estimatedArrival': u'2018-11-24T11:25:03Z', u'lng': 6.54436, u'id': u'end_wp', u'fulfilledConstraints': []}], u'timeBreakdown': {u'rest': 0, u'service': 0, u'driving': 5477, u'waiting': 0}, u'time': u'5477'}], u'requestId': None, u'responseCode': u'200', u'processingTimeDesc': u'54912ms'}

# print len(resp['results'])

waypoints = list()

for wp in resp['results'][0]['waypoints']:
    print wp #['lat'], wp['lng']
    waypoints.append("%f,%f" % (wp['lat'], wp['lng']))

waypoints_to_image(waypoints)

# pickup_optimizer()