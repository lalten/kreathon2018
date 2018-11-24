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

# add_all_containers()


def all_empty():
    for c in Container.objects.all():
        m = Measurement(container=c, raw_reading=c.reading_sonic_empty+0.1)
        m.save()

# all_empty()

def fill(c_id, reading = 0.0):
    c = Container.objects.get(id=c_id)
    m = Measurement(container=c, raw_reading=reading)
    m.save()


fill(53)
fill(9)
fill(43)
fill(25)
fill(29)
fill(52)

fill(66, 0.2)
fill(65, 0.2)
fill(51, 0.2)




