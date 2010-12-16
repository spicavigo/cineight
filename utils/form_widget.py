#!/usr/bin/env python
#
#       widget.py
#       

from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

class ImageInput(Widget):
    
    def render(self, name, value, attrs=None):
        value = (value and ('<img src="'+value.url+'"></img>')) or 'No Image uploaded as yet'
        final_attrs = self.build_attrs(attrs, type='file', name=name)        
        return mark_safe(u'<input%s /> %s' % (flatatt(final_attrs), value))


