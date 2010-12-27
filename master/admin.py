#!/usr/bin/env python
#
#       admin.py
#       
#       Copyright 2009 Yousuf Fauzan <yousuffauzan@gmail.com>
#       

from django.contrib import admin
from master.models import *

admin.site.register(List)
admin.site.register(PublicList)