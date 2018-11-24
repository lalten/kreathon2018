# app_id = "nAX0YLEqe9rDAffuvS9L"
# app_code = "O_9Z4uw6cbqaUNKCrWvAlg"

# app_id = "KPsWibxDNxMleCgVgsaB"
# app_code = "Id0sT7rAiKu5Hx-Y0GdN8g"

app_id = "9QUQ9EMEU9Ex8wYShCOu"
app_code = "0FLZ9442aCDEqBa1Xw3xwQ"
import requests

monday_route = [17, 96, 45, 19, 21, 30, 35, 23, 26, 25, 44,
                27, 28, 31, 33, 91, 66, 43, 36, 67, 38, 39, 46, 40, 48, 9, 52, 12, 15, 55, 86, 57, 90, 88]

calc_route_url = "https://route.api.here.com/routing/7.2/calculateroute.json"
route_url = "https://image.maps.api.here.com/mia/1.6/route"


def waypoints_to_image(way_points):
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
    app_data['lc'] = 'ffff0000'
    app_data['sc'] = 'ffff0000'
    app_data['mlbl'] = 0

    # app_data['ctr'] = way_points[0]

    app_data['lw'] = 10  # line width

    r = requests.get(route_url, app_data)

    f = open('/tmp/route.jpg', 'wb')
    f.write(r.content)
    f.close()

    return r.url


def route_to_image(route):
    legs = route['response']['route'][0]['leg']
    # print len(legs)
    way_points = list()
    for leg in legs:
        for l in leg['maneuver']:
            way_points.append("%f,%f" % (l['position']['latitude'], l['position']['longitude']))
    return waypoints_to_image(way_points)

def calc_route(positions, mode='car'):
    app_data = {"app_id": app_id, "app_code": app_code}
    app_data['mode'] = 'fastest;'+mode+';traffic:disabled'

    for i, p in enumerate(positions):
        app_data['waypoint' + str(i)] = p
        # if i == 10:
        #     break

    # print (app_data)
    r = requests.get(calc_route_url, app_data)
    # r = requests.get(route_url, app_data)

    # print r.status_code
    # print r.json()

    route = r.json()
    return route