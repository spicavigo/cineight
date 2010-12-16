#!/usr/bin/env python
#
#       cineight.wsgi
#
#       Copyright 2010 yousuf <yousuf@postocode53.com>
#

# note that the above directory depends on the locale of your virtualenv,
# and will thus be *different for each project!*
import os
import sys
import site

prev_sys_path = list(sys.path)

new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
       new_sys_path.append(item)
       sys.path.remove(item)
sys.path[:0] = new_sys_path

# this will also be different for each project!
sys.path.append('/home/django/domains/cineight.com/cineight/')

os.environ['PYTHON_EGG_CACHE'] = '/home/django/.python-eggs'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

sys.stdout=sys.stderr
