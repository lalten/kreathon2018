#! /usr/bin/python
# coding: utf8

import requests
import Levenshtein


fname = '/home/engelhard/Documents/kreathon2018/locations.csv'


f = open(fname, 'r')
lines = f.readlines()

app_id = "nAX0YLEqe9rDAffuvS9L"
app_code = "O_9Z4uw6cbqaUNKCrWvAlg"

# map_view_url = "https://image.maps.api.here.com/mia/1.6/mapview"
# auto_suggest_url = "https://places.cit.api.here.com/places/v1/autosuggest"
auto_suggest_url = "https://places.cit.api.here.com/places/v1/discover/search"




def auto_suggest(query):
    app_data = {"app_id": app_id, "app_code": app_code}
    app_data['at'] = "51.33,6.58"  # Krefeld
    app_data['q'] = query

    # print app_data

    r = requests.get(auto_suggest_url, app_data)
    if r.status_code != 200:
        print ("ERROR: ", r.status_code)
        return None

    # print r.status_code
    # print r.json()

    results = r.json()['results']
    if not results:
        print "no result for", query
        return None

    # print results['items'][0]['position']

    # print results.items()[0][0]

    # print "ASD"
    # print results

    best_result = None
    best_score = -1
    i = 0
    positions = list()
    for item in results['items']:
        dist = float(item['distance'])
        if dist > 8000:
            print ("large dist: %f" % dist)
            continue

        title = item['title']
        position = item['position']

        positions.append(position)
        print i, title, position
        i += 1


    ans = int(raw_input("which to choose?") or '0')
    if ans == -1:
        return None
    else:
        return positions[ans]
    # print ans
    # print str_score
    # print best_result['position']
    # return best_result




locations = dict()


for l in lines:
    if 'Tourfolge' in l or len(l) < 10:
        continue
    spl = l.split(';')
    assert len(spl) == 7
    location_description = spl[1]+ ", " + spl[2]
    # print location_description
    ids = map(int, [x.strip() for x in spl[6].split(',')])
    main_id = ids[0]  # lookup only for first container in group

    # multiple entries for 24
    if main_id == 24:
        continue

    if main_id in locations:
        if not location_description == locations[main_id]:
            print main_id
            print location_description
            print locations[main_id]
    else:
        locations[main_id] = location_description

p = dict()

p[1] = "51.33608,6.63602"
p[2] = "51.348621,6.64751"
p[3] = "50.221108, 8.621942"
p[4] = "51.36249,6.62339"
p[5] = "51.36316,6.59766"
p[8] = "51.3358,6.64371"
p[9] = "51.330259, 6.545865"
p[10] = "51.3165, 6.57619"
p[12] = "51.339211, 6.55931"
p[15] = "51.34465, 6.54805"
p[17] = "51.339626, 6.617302"
p[18] = "51.32936, 6.62697"
p[19] = "51.31898, 6.62664"
p[21]="51.316460, 6.602660"
p[23]="51.319230, 6.588010"
p[25]="51.322891, 6.580700"
p[26]="51.316500, 6.576190"
p[43] = "51.330220, 6.565961"
p[28]="51.312031,6.558730"
p[28]="51.312031,6.558730"
p[29]="51.308300,6.565790"
p[30]="51.308690,6.589100"
p[31]="51.305210,6.583580"
p[33]="51.303040,6.580220"
p[34]="51.294910,6.586550"
p[35]="51.316479,6.589900"
p[36]="51.331768,6.578997"
p[38]="51.345242,6.590920"
p[39]="51.343110,6.568970"
p[40]="51.334660,6.563870"
p[44]="51.318310,6.561890"
p[45]="51.333940,6.600560"
p[46]="51.336491,6.570110"
p[48]="51.335980,6.556940"
p[50]="51.334492,6.565060"
p[51]="51.320970,6.546540"
p[52]="51.321080,6.527850"
p[53]="51.329960,6.536940"
p[54] = "51.344067, 6.552482"
p[55] = "51.349869, 6.552332"
p[56] = "51.346430, 6.545919"
p[57] = "51.452205, 6.638454"
p[75] = "51.331713, 6.679759"
p[64]="51.351270,6.650410"
p[65]="51.333450,6.572000"
p[66]="51.325859,6.557780"
p[67]="51.338820,6.574970"
p[69]="51.363541,6.614750"
p[71]="51.320389,6.563060"
p[73] = "51.329617, 6.670257"
p[76]="51.337009,6.660000"
p[77]="51.344158,6.641220"
p[78]="51.358160,6.646050"
p[79]="51.362070,6.573890"
p[80]="51.336460,6.547930"
p[82]="51.340721,6.537810"
p[83]="51.334301,6.546460"
p[84]="51.348358,6.527010"
p[85]="51.347480,6.520020"
p[86]="51.363708,6.521440"
p[88] = "51.370293, 6.497376"
p[90]="51.371940,6.497830"
p[91]="51.320091,6.552320"
p[96]="51.341310,6.599210"


# ofile = file('poses.txt', 'aw')
#
#
# print "Number of locations", len(locations)
# for i, l in enumerate(locations):
#     if l in p:
#         continue
#
#     s = locations[l]
#
#     print l, "->", s
#     sug = auto_suggest(s)
#     if not sug:
#         continue
#
#     p[l] = sug
#     s = "%f,%f" % (sug[0], sug[1])
#     ofile.write('p[%i]="%s"' % (l, s) + '\n')
