#! /usr/bin/python

import django
django.setup()
from backend.models import Measurement, Container

print ("Number of Containers: %i" % Container.objects.count())
print ("Number of Measurements: %i" % Measurement.objects.count())


def add_all_containers():
    f = open('/home/engelhard/Documents/kreathon2018/geo_locations.txt')
    for l in f.readlines():
        id_s, pos_str, location = l.split(':')
        id = int(id_s)
        lat, lng = map(float, pos_str.split(','))
        # print id, lat, lng, location
        c = Container(id=id, lat=lat, lng=lng, location_string=location)
        print c
        c.save()

add_all_containers()
