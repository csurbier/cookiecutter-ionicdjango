# coding: utf8
from __future__ import unicode_literals
from bo.models import *
import logging
from swiitch.settings import GOOGLE_DISTANCE_API_KEY
from django.utils import timezone
# Get an instance of a logger
logger = logging.getLogger('django')
import asyncio
from bo.partners.heech import getHeetchResuls
from bo.partners.bolt import getBoltResuls
from bo.partners.kapten import getKaptenResuls
from bo.partners.marcel import getMarcelResuls

"""
async def getLeCabResuls(future):
    print("One")
    gmaps = googlemaps.Client(key=GOOGLE_DISTANCE_API_KEY)
    search = Search.objects.get(id="65b96ed5-7a0c-4cd2-a35b-32531c6c40ec")
    origins = [{"lat": search.locationStart.y, "lng": search.locationStart.x}]
    destinations = [
        {"lat": search.locationDestination.y, "lng": search.locationDestination.x}]
    matrix = gmaps.distance_matrix(origins, destinations)

    try:
        if matrix:
            rows = matrix["rows"]
            elements = rows[0]
            element = elements["elements"]
            data = element[0]
            logger.info("%s" % data)
            distance = data["distance"]
            duration = data["duration"]
            distanceValue = distance["value"]

            durationValue = duration["value"]
            destinationA = {"lat": search.locationStart.y,
                            "lng": search.locationStart.x}
            destinationB = {"lat": search.locationDestination.y,
                            "lng": search.locationDestination.x}
            direction = gmaps.directions(destinationA, destinationB, mode="driving")
            logger.info("On recoit %s" % direction)
            resultat = "DONE"
            future.set_result(resultat)
    except Exception as e:
        logger.error(e)
"""

def run():
    import urllib
    search = Search.objects.get(id="2eef89a1-470b-4cf7-9d62-e54aaa58526e")
    print(search.locationStart.y)
    print(search.locationStart.x)
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(getMarcelResuls(future,search))
    loop.run_until_complete(future)
    print(future.result())

