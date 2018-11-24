import requests
import json

goal_seconds = 4 * 60 * 60
max_distance = 30 * 60 #max 30 Minuten Abweichung
app_id ="nAX0YLEqe9rDAffuvS9L"
app_code="O_9Z4uw6cbqaUNKCrWvAlg"

route_url = "https://image.maps.api.here.com/mia/1.6/route"

def route_to_image(route):
    #    legs = route['response']['route'][0]['leg']
    #    # print len(legs)
    #    way_points = list()
    #    for leg in legs:
    #        for l in leg['maneuver']:
    #            way_points.append("%f,%f" % (l['position']['latitude'], l['position']['longitude']))
    #
    print(route)
#    way_point_str = ",".join(route)
    way_point_str =""
    for r in route:
        way_point_str += "%f,%f," % (r['lat'], r['lng'])
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

def make_tsp_calculation(l):
    start_point = {'lat' : '51.3304', 'lng': '6.54436'}

    base_url = "https://route.api.here.com/routing/7.2/calculateroute.json?app_id=nAX0YLEqe9rDAffuvS9L&app_code=O_9Z4uw6cbqaUNKCrWvAlg&mode=shortest;car;traffic:disabled"
    base_url += "&waypoint0=geo!" + start_point['lat'] + "," + start_point['lng']

    idx = 1 
    for item in l:
        base_url += "&waypoint" + str(idx) + "=geo!" +str(item['lat']) + "," + str(item['lng'])
        idx += 1

    base_url += "&waypoint" + str(idx) + "=geo!" + start_point['lat'] + "," + start_point['lng']

    resp = json.loads(requests.get(base_url).text)['response']
    route = resp['route'][0]
    summary = route['summary']
    time = summary['trafficTime']
    return (time, route)
    
def route_to_waypoints(route):
    result = []
    for w in route['waypoint']:
        lat = w['mappedPosition']['latitude']
        lng = w['mappedPosition']['longitude']
        result.append({'lat' : lat, 'lng' : lng})
    return result

    

        

def get_for_treshold(data, treshold):
    result = []
    for c in data:
        if c['level'] >= treshold:
            result.append(c)

    return result


def get_data():
    data = requests.get("http://10.13.144.90:5000/containers")
    data =json.loads(data.text)['containers']
    return data



def start():
    #define start time
    time = 0

    #start treshold
    treshold = 95 #full

    #aquire data
    data = get_data()
    route = None

    while time < goal_seconds:
        route_data = get_for_treshold(data, treshold)
        time, route = make_tsp_calculation(route_data)
        print("Treshold: %d, Anzahl Container: %d, Benötigte Zeit: %d, Abweichung: %d" % (treshold, len(route_data), time, abs(time-goal_seconds)))
        treshold -= 5
    
    print("Optimal: %d" % time)

    coordinates = route_to_waypoints(route)
    route_to_image(coordinates)

start()




