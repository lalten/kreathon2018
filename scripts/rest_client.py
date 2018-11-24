#! /usr/bin/python
# coding: utf8


import requests
from sequence_optimization import calc_route, route_to_image

# url = 'http://10.13.144.90:5000/containers'
# data_dict = {"user":"asddd"}
#
# response = requests.get(url, data_dict)
# print response.json()['containers'][0]

# url = 'http://10.13.144.90:5000/feedback'
# data_dict = {"user_id": 123, "first_name": "horst", "lat": 51.312031, "lng": 6.558730, "clean": 3}
# response = requests.post(url, data_dict)



# ask for closest container and show route to it
url = 'http://10.13.144.90:5000/get_closest'
data_dict = {"lat": 51.33, 'lng': 6.6}

response = requests.post(url, data_dict)

js = response.json()['best_container']

pos = js['closest_container_pos']
dist = js['dist']
print "dist", dist
s = ["%f,%f" % (data_dict['lat'], data_dict['lng']), pos]
route = calc_route(s, 'pedestrian')
route_to_image(route)
