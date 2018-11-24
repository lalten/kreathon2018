#! /usr/bin/python
# coding: utf8

import django
django.setup()
from backend.models import Container

import requests

from here_connector import *

def get_positions(route):
    positions = list()
    for r in route:
        try:
            c = Container.objects.get(id=r)
        except Container.DoesNotExist:
            print r, "no position"
            continue

        positions.append("%f,%f" % (c.lat, c.lng))
    return positions



# positions = get_positions(monday_route)
#
# start=positions[10]
# for i, p in enumerate(positions):
#     # if i == 0:
#     #     continue
#     # print start, p
#
#     r = calc_route([start, p])
#     d_sum = 0
#     for m in r['response']['route'][0]['leg'][0]['maneuver']:
#         d_sum += m['length']
#
#     print d_sum


    # break










# route = calc_route(positions)
#
# print route
#
# route_to_image(route)

#
#
#
# # print monday_route
#
# # sequence_url = "https://wse.cit.api.here.com/2/findsequence.json"
#
#
# def find_sequence(self):
#     app_data = {"app_id": self.app_id, "app_code": self.app_code}
#     app_data['start'] = self.loc_to_waypoint(self.container_locations[0])
#     for i, cl in enumerate(self.container_locations):
#         if i == 0:
#             continue
#         app_data['destination' + str(i)] = self.loc_to_waypoint(cl)
#         if i == 10:
#             break
#
#     app_data['end'] = self.loc_to_waypoint(self.container_locations[-1])
#     app_data['mode'] = 'truck;fastest'
#     # print app_data
#
#     # print time.time()
#     s = Session()
#     req = Request('GET', url=self.sequence_url, params=app_data).prepare()
#     print (req.url)
#
#     r = s.send(req)
#
#     # r = requests.get(self.sequence_url, app_data)
#
#     # print time.time()
#     # print r.url
#     # print r.status_code
#     print (r.json())
#
#

#
# def find_sequence(self):
#     app_data = {"app_id": self.app_id, "app_code": self.app_code}
#     app_data['start'] = self.loc_to_waypoint(self.container_locations[0])
#     for i, cl in enumerate(self.container_locations):
#         if i == 0:
#             continue
#         app_data['destination' + str(i)] = self.loc_to_waypoint(cl)
#         if i == 10:
#             break
#
#     app_data['end'] = self.loc_to_waypoint(self.container_locations[-1])
#     app_data['mode'] = 'truck;fastest'
#     # print app_data
#
#     # print time.time()
#     s = Session()
#     req = Request('GET', url=self.sequence_url, params=app_data).prepare()
#     print (req.url)
#
#     r = s.send(req)
#
#     # r = requests.get(self.sequence_url, app_data)
#
#     # print time.time()
#     # print r.url
#     # print r.status_code
#     print (r.json())
#
#
# def route_to_image(self):
#     legs = self.route['response']['route'][0]['leg']
#     # print len(legs)
#     way_points = list()
#     for leg in legs:
#         for l in leg['maneuver']:
#             way_points.append("%f,%f" % (l['position']['latitude'], l['position']['longitude']))
#
#     way_point_str = ",".join(way_points)
#     # print way_point_str
#
#     app_data = {"app_id": self.app_id, "app_code": self.app_code}
#     app_data['h'] = 1024
#     app_data['w'] = 1024
#     app_data['ppi'] = 320
#     app_data['t'] = 3
#     app_data['z'] = 17  # zoom level: 20: Haus, 6: Europa
#
#     app_data['r'] = way_point_str
#     app_data['m'] = way_point_str
#     app_data['lc'] = '440000ff'
#     app_data['sc'] = '440000ff'
#     app_data['mlbl'] = 0
#
#     # app_data['ctr'] = way_points[0]
#
#     app_data['lw'] = 20  # line width
#
#     r = requests.get(self.route_url, app_data)
#     print (r.url)
#
#     # print r.content
#
#     # print r.status_code
#     f = open('/tmp/route.jpg', 'wb')
#     f.write(r.content)
#     f.close()
