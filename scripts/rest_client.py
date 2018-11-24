#! /usr/bin/python
# coding: utf8


import requests

url = 'http://10.13.144.90:5000/containers'
data_dict = {"user":"asddd"}

response = requests.get(url, data_dict)
print response.json()['containers'][0]

