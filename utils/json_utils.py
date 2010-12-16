#!/usr/bin/env python
#
#       json_utils.py
#       

from django.http import HttpResponse
import json

class JsonResponse(HttpResponse):
    def __init__(self, content):
        super(JsonResponse, self).__init__(content=content,
                                           mimetype='application/json')
