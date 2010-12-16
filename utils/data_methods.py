#!/usr/bin/env python
#
#       data_methods.py
#       
#       Copyright 2009 yousuf <yousuf@postocode53.com>
#
from django.conf import settings
from django.core.cache import cache
from django.utils.safestring import mark_safe
import json
import re
import time

import cPickle as pickle
    
class Memoize(object):
    def __init__(self, keyfunc):
        self.keyfunc = keyfunc

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            if 'get_key' in kwargs:
                del kwargs['get_key']
                return pickle.dumps((fn.func_name, self.keyfunc(*args, **kwargs)))
                
            if not wrapped.func_dict.get('state', None):
                wrapped.state = {}
            if 'reset' in kwargs:
                del kwargs['reset']
                key = pickle.dumps((fn.func_name, self.keyfunc(*args, **kwargs)))
                wrapped.state[key] = 0
                
            key = pickle.dumps((fn.func_name, self.keyfunc(*args, **kwargs)))
            if wrapped.state.get(key,0) == 0:
                wrapped.state[key] = time.time()
                cache.delete(key)
            for f, state in wrapped.func_dict.get('depends',{}).items():
                    if f.state[state[0]] != state[1]:
                        cache.delete(key)

            value = cache.get(key)
            if not value:
                value = fn(*args, **kwargs)                
                cache.set(key, pickle.dumps(value))
            else:
                value = pickle.loads(value)
            return value
        return wrapped

def get_exclude_dict():
    apps = settings.LZ_APPS[1:]
    output = {}
    for app in apps:
        app = app[0]
        output[app] = {'value': False, 'classes':{}}
        page = __import__(app + '.page', fromlist=[app])
        box = __import__(app + '.box', fromlist=[app])
        widget = __import__(app + '.widget', fromlist=[app])
        tab = __import__(app + '.tab', fromlist=[app])
        pages = [page.__name__ + '.' + e for e in dir(page) if e.endswith('Page') and getattr(page,e).__module__==page.__name__]
        boxes = [box.__name__ + '.' + e for e in dir(box) if e.endswith('Box') and getattr(box,e).__module__==box.__name__]
        widgets = [widget.__name__ + '.' + e for e in dir(widget) if e.endswith('Widget') and getattr(widget,e).__module__==widget.__name__]
        tabs = [tab.__name__ + '.' + e for e in dir(tab) if e.endswith('Tab') and getattr(tab,e).__module__==tab.__name__]
        output[app]['classes'] = dict.fromkeys(pages+boxes+widgets+tabs, False)
    return output

def merge(init_dict, new_data):
    for module, value in init_dict.items():
        if module in new_data:
            init_dict[module]['value'] = True
        for cls in value['classes'].keys():
            if cls in new_data:
                init_dict[module]['classes'][cls] = True
    return init_dict

def get_excludes(user):
    try:
        up = getattr(user, 'userprofile', None)
        return json.loads(up.primary_university.exclude_objects or '[]')
    except Exception, e:
#        print "Error"
#        print e
        pass
    return []


def slugify(value,replace_with='_'):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return mark_safe(re.sub('[-\s]+', replace_with, value))