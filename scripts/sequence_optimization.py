#! /usr/bin/python
# coding: utf8

import django
django.setup()
from backend.models import Container

import requests

app_id = "nAX0YLEqe9rDAffuvS9L"
app_code = "O_9Z4uw6cbqaUNKCrWvAlg"

monday_route = [17, 96, 45, 19, 21, 30, 35, 23, 26, 25, 44,
                27, 28, 31, 33, 91, 66, 43, 36, 67, 38, 39, 46, 40, 48, 9, 52, 12, 15, 55, 86, 57, 90, 88]

calc_route_url = "https://route.api.here.com/routing/7.2/calculateroute.json"
route_url = "https://image.maps.api.here.com/mia/1.6/route"


def route_to_image(route):
    legs = route['response']['route'][0]['leg']
    # print len(legs)
    way_points = list()
    for leg in legs:
        for l in leg['maneuver']:
            way_points.append("%f,%f" % (l['position']['latitude'], l['position']['longitude']))

    way_point_str = ",".join(way_points)
    # print way_point_str

    app_data = {"app_id": app_id, "app_code": app_code}
    app_data['h'] = 1024
    app_data['w'] = 1024
    app_data['ppi'] = 320
    app_data['t'] = 3
    app_data['z'] = 17  # zoom level: 20: Haus, 6: Europa

    app_data['r'] = way_point_str
    app_data['m'] = way_point_str
    app_data['lc'] = '440000ff'
    app_data['sc'] = '440000ff'
    app_data['mlbl'] = 0

    # app_data['ctr'] = way_points[0]

    app_data['lw'] = 10  # line width

    r = requests.get(route_url, app_data)
    print (r.url)

    # print r.content

    # print r.status_code
    f = open('/tmp/route.jpg', 'wb')
    f.write(r.content)
    f.close()



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

def calc_route(positions):
    app_data = {"app_id": app_id, "app_code": app_code}
    app_data['mode'] = 'fastest;car;traffic:disabled'

    for i, p in enumerate(positions):
        app_data['waypoint' + str(i)] = p
        if i == 10:
            break

    print (app_data)
    r = requests.get(calc_route_url, app_data)
    # print r.status_code
    # print r.json()

    route = r.json()
    return route

positions = get_positions(monday_route)

route = calc_route(positions)

print route

route_to_image(route)

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
