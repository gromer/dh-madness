from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from stravaapi import StravaApi

def index(request):
    api = StravaApi()

    ride_stream = api.ride_stream(6206631)

    context = RequestContext(request)
    return render_to_response('dhmadness/index.html',
        {
            'ride_stream': ride_stream
        },
        context_instance=context)
