#! /usr/bin/python
# coding: utf8

from requests import Request, Session
import requests
import Levenshtein
import io
import time

class HereConector:
    app_id = "nAX0YLEqe9rDAffuvS9L"
    app_code = "O_9Z4uw6cbqaUNKCrWvAlg"

    map_view_url = "https://image.maps.api.here.com/mia/1.6/mapview"
    auto_suggest_url = "https://places.cit.api.here.com/places/v1/autosuggest"
    # sequence_url = "https://wse.api.here.com/2/findsequence.json"
    sequence_url = "https://wse.cit.api.here.com/2/findsequence.json"
    calc_route_url = "https://route.api.here.com/routing/7.2/calculateroute.json"

    # route_url = "https://image.maps.api.here.com/mia/1.6/route"
    route_url = "https://image.maps.api.here.com/mia/1.6/route"

    def __init__(self):
        pass
        # print self.container_locations

    def all_auto(self):
        with io.open("inseln.txt", "r", encoding="utf-8") as my_file:
            lines = my_file.read().split('\n')

        locations = list()

        for l in lines:
            s = l.rstrip()
            if len(s) == 0:
                continue
            print ("#############################################################")
            best_hit = self.auto_suggest(query=s)
            if not best_hit:
                print ("Could not process ", s)
                continue

            locations.append((best_hit['title'], best_hit['position']))

        print (locations)

    def auto_suggest(self, query):
        app_data = {"app_id": self.app_id, "app_code": self.app_code}
        app_data['at'] = "48.1347,11.5126" # Laim
        app_data['q'] = query

        r = requests.get(self.auto_suggest_url, app_data)
        if r.status_code != 200:
            print ("ERROR: ", r.status_code)
            return None

        results = r.json()['results']
        if not results:
            return None

        best_result = None
        best_score = -1
        for r in results:
            title = r['title']
            str_score = Levenshtein.ratio(query, title)
            if str_score > best_score:
                best_result = r
                best_score = str_score

        # print str_score
        # print best_result['position']
        return best_result

    def all_images(self):
        for c in self.container_locations:
            name = c[0].replace(' ', '_').replace('/', '_')

            f_path = '/tmp/' + name + '.jpg'
            print (f_path)

            self.get_map_view(c[1], f_path)

            # break

    def loc_to_waypoint(self, location):
        return str(location[1][0]) + ',' + str(location[1][1])

    def calc_route(self):
        app_data = {"app_id": self.app_id, "app_code": self.app_code}
        app_data['mode'] = 'fastest;car;traffic:disabled'
        for i, cl in enumerate(self.container_locations):
            app_data['waypoint' + str(i)] = self.loc_to_waypoint(cl)
            if i == 10:
                break

        print (app_data)
        r = requests.get(self.calc_route_url, app_data)
        # print r.status_code
        # print r.json()

        route = r.json()
        return route




    def find_sequence(self):
        app_data = {"app_id": self.app_id, "app_code": self.app_code}
        app_data['start'] = self.loc_to_waypoint(self.container_locations[0])
        for i, cl in enumerate(self.container_locations):
            if i == 0:
                continue
            app_data['destination' + str(i)] = self.loc_to_waypoint(cl)
            if i == 10:
                break

        app_data['end'] = self.loc_to_waypoint(self.container_locations[-1])
        app_data['mode'] = 'truck;fastest'
        # print app_data

        # print time.time()
        s = Session()
        req = Request('GET', url=self.sequence_url, params=app_data).prepare()
        print (req.url)

        r = s.send(req)

        # r = requests.get(self.sequence_url, app_data)

        # print time.time()
        # print r.url
        # print r.status_code
        print (r.json())

    def route_to_image(self):
        legs = self.route['response']['route'][0]['leg']
        # print len(legs)
        way_points = list()
        for leg in legs:
            for l in leg['maneuver']:
                way_points.append("%f,%f" % (l['position']['latitude'], l['position']['longitude']))

        way_point_str = ",".join(way_points)
        # print way_point_str

        app_data = {"app_id": self.app_id, "app_code": self.app_code}
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

        app_data['lw'] = 20 # line width

        r = requests.get(self.route_url, app_data)
        print (r.url)

        # print r.content

        # print r.status_code
        f = open('/tmp/route.jpg', 'wb')
        f.write(r.content)
        f.close()

    def get_map_view(self, long_lat, file_path):
        app_data = {"app_id": self.app_id, "app_code": self.app_code}
        app_data['h'] = 512
        app_data['w'] = 512
        app_data['ppi'] = 320
        app_data['t'] = 3
        # app_data['t'] = 3  # Satellite map view with streets in day light mode.
        app_data['z'] = 16  # zoom level: 20: Haus, 6: Europa

        # app_data['ci'] = "Munich"

        app_data['lat'] = long_lat[0]
        app_data['lon'] = long_lat[1]

        # app_data['s'] = "Friedenheimer Straße" #  / Agnes-Bernauer-Straße"
        # app_data['s'] = 'Agnes-Bernauer-Straße'
        #app_data['n'] = '234'
        #app_data['zi'] = 80687  # PLZ definiert Ausschnitt

        r2 = requests.get(self.map_view_url, app_data)
        # print r2.content

        f = open(file_path, 'wb')
        f.write(r2.content)
        f.close()

if __name__ == "__main__":
    hc = HereConector()
    # hc.get_map_view('/tmp/asd.jpg')
    # hc.auto_suggest("Hauzenberger Straße/ Elsenheimerstraße")
    # hc.all_auto()
    # hc.all_images()
    hc.find_sequence()
    # print hc.calc_route()
    # hc.route_to_image()