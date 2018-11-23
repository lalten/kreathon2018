#! /usr/bin/python

import django
django.setup()
from backend.models import Measurement, Container

print ("Number of Containers: %i" % Container.objects.count())
print ("Number of Measurements: %i" % Measurement.objects.count())
