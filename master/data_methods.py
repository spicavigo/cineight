from master.models import *
from django.conf import settings
import base64
import hashlib
import hmac
try:
    import json
except ImportError:
    import simplejson as json

def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor 
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def parse_signed_request(signed_request):
    secret = settings.FACEBOOK_SECRET_KEY
    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        return data
    
def tweet(movie, rating):
    if rating < 0:
        settings.API.update_status('#Warned - %s #movie #cineight' % str(movie))
    else:
        settings.API.update_status('#Recommended - %s #movie #cineight' % str(movie))
    

