from master.models import *
from django.conf import settings

def tweet(movie, rating):
    if rating < 0:
        settings.API.update_status('#Warned - %s #movie #cineight' % str(movie))
    else:
        settings.API.update_status('#Recommended - %s #movie #cineight' % str(movie))
