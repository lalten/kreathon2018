#! /usr/bin/python
# coding: utf8


import requests

# url = 'http://10.13.144.90:5000/containers'
# data_dict = {"user":"asddd"}
#
# response = requests.get(url, data_dict)
# print response.json()['containers'][0]

url = 'http://10.13.144.90:5000/feedback'
data_dict = {"user_id": 123, "first_name": "horst", "lat": 51.312031, "lng": 6.558730, "clean": 3}
response = requests.post(url, data_dict)