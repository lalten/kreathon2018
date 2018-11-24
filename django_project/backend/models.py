from __future__ import unicode_literals

from django.db import models
import datetime


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50, default="no_first_name")


class Container(models.Model):
    # id
    lng = models.FloatField(default=-1)
    lat = models.FloatField(default=-1)
    location_string = models.CharField(max_length=300, default="no_location_string")

    # recursive Fkey: https://docs.djangoproject.com/en/dev/ref/models/fields/#foreignkey
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    # raw reading for super sonic sensor for empty and full
    reading_sonic_empty = models.FloatField(default=1.0)
    reading_sonic_full = models.FloatField(default=0.0)

    def reading_in_range(self, reading):
        min_ = min(self.reading_sonic_full, self.reading_sonic_empty)
        max_ = max(self.reading_sonic_full, self.reading_sonic_empty)

        if not (min_ <= reading <= max_):
            print ("READING NOT IN RANGE: %f, %f, %f" % (min_, reading, max_))
            return False

        return True

    def __str__(self):
        return "Container %i at %.5f %.5f, empty: %.2f, full: %.2f" % (self.id, self.lat, self.lng,
                                                                self.reading_sonic_empty,
                                                                self.reading_sonic_full)

class Measurement(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    raw_reading = models.FloatField(default=-1)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        time_str = self.date.strftime("%Y-%m-%d %H:%M:%S")
        return "Measurement id %i for container %i, reading: %.2f at %s" % (self.id, self.container.id,
                                                                            self.raw_reading, time_str)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    container = models.ForeignKey(Container, null=True, on_delete=models.CASCADE)  # null if to far from any Container

    lng = models.FloatField(null=True, blank=True, default=None)
    lat = models.FloatField(null=True, blank=True, default=None)

    rating = models.IntegerField(default=-1)
    message = models.CharField(max_length=500, default="no_message")


# User:
# id: pkey(von
# telegram)
# first_name: CharField
#
# BottleBank:
# id: pkey(autogenerated)
# lng: Float
# lat: Float
#
# Container:
# bank: fkey -> Bottlebank
# glasColor: int(w, g, b)
# reading_empty: Float
# reading_full: Float
#
# Measurement:
# container_id: fkey -> Container
# raw_reading: Float
# date: Date(automatic
# on
# creation)
#
# Feedback:
# user_id: fkey
# raw_location_lng: Float
# raw_location_lat: Float
# bank_id: fkey
# rating: int
# message: CharField(Freitext?)
#
#
#
# Interface
# Chat
# to
# DB: (ziemlich klein -> REST)
#
# post: / feedback(user_id, lng, lat, rating, msg) -> is_valid_position
# get: / get_empty_locations() -> all
# non - full
# Banks
# with location(fuer here visualization)
#
# ChatBot:
#
# / feedback -> LocationRequest -> Frage
# nach
# Sauberkeit(optional
# noch
# freitext)
# / nextContainer -> LocationRequest -> Karte
# mit
# Fussweg(mit
# Link
# zur
# website) (keine Frage nach TransportationMode -> zu viel Zeit in Demo)