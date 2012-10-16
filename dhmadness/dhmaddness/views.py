from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from stravaapi import StravaApi


METERS_TO_MILES_RATIO = 0.000621371
METERS_TO_FEET_RATIO = 3.28084
KILOMETERS_PER_SECOND_TO_MILES_PER_HOUR_RATIO = 0.621371
METERS_PER_SECOND_TO_MILES_PER_HOUR_RATIO = 2.23694
SECONDS_TO_MINUTES_RATIO = 0.0166667


def index(request, ride_id=None):
    if ride_id is None:
        ride_id = 6206631

    api = StravaApi()

    ride_stream = api.ride_stream(ride_id)

    points = []

    altitudes = ride_stream['altitude']
    #altitude_originals = ride_stream['altitude_original']
    distances = ride_stream['distance']
    grade_smooths = ride_stream['grade_smooth']
    latlngs = ride_stream['latlng']
    movings = ride_stream['moving']
    outliers = ride_stream['outlier']
    times = ride_stream['time']
    velocity_smooths = ride_stream['velocity_smooth']
    watts_calcs = ride_stream['watts_calc']

    number_of_points = len(altitudes)

    for i in range(number_of_points):
        altitude = altitudes[i]
        #altitude_original = altitude_originals[i]
        distance = distances[i]
        grade_smooth = grade_smooths[i]
        latlng = latlngs[i]
        moving = movings[i]
        outlier = outliers[i]
        time = times[i]
        velocity_smooth = velocity_smooths[i]
        watts_calc = watts_calcs[i]

        point = {
            'altitude': altitude * METERS_TO_FEET_RATIO,
            #'altitude_original': altitude_original * METERS_TO_FEET_RATIO,
            'distance': distance * METERS_TO_MILES_RATIO,
            'grade_smooth': grade_smooth,
            'latlng': latlng,
            'moving': moving,
            'outlier': outlier,
            'time': time,
            'velocity_smooth': velocity_smooth * METERS_PER_SECOND_TO_MILES_PER_HOUR_RATIO,
            'watts_calc': watts_calc,
        }

        points.append(point)

    stats = {
        'altitude': get_stats(altitudes, 'ft', 'Altitude'),
        'grade_smooth': get_stats(grade_smooths, '%', 'Grade'),
        'velocity_smooth': get_stats(velocity_smooths, 'mi/hr', 'Speed'),
        'watts_calc': get_stats(watts_calcs, 'w', 'Power'),
    }

    stats['altitude']['min'] *= METERS_TO_FEET_RATIO
    stats['altitude']['average'] *= METERS_TO_FEET_RATIO
    stats['altitude']['max'] *= METERS_TO_FEET_RATIO
    stats['velocity_smooth']['min'] *= METERS_PER_SECOND_TO_MILES_PER_HOUR_RATIO
    stats['velocity_smooth']['average'] *= METERS_PER_SECOND_TO_MILES_PER_HOUR_RATIO
    stats['velocity_smooth']['max'] *= METERS_PER_SECOND_TO_MILES_PER_HOUR_RATIO

    ride_distance = max(distances) * METERS_TO_MILES_RATIO

    context = RequestContext(request)
    return render_to_response('dhmadness/index.html',
        {
            'points': points,
            'stats': stats,
            'ratios': {
                'seconds_to_minutes': SECONDS_TO_MINUTES_RATIO,
            },
            'ride_distance': ride_distance
        },
        context_instance=context)


def get_stats(collection, measurement, display):
    if collection is None or len(collection) == 0:
        return {'average': 0, 'min': 0, 'max': 0, 'measurement': '', 'display': ''}

    average_value = sum(collection) / len(collection)
    min_value = min(collection)
    max_value = max(collection)

    return {
        'average': average_value,
        'min': min_value,
        'max': max_value,
        'measurement': measurement,
        'display': display
    }