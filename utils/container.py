#!/usr/bin/env python
#
#       container.py
#       
from django.template import Context
from django.template.loader import get_template
       
class Container(object):        
    def show(self, template, context, is_json=False):
        context = context or self.context
        if is_json:
            return context
        template = template or self._media.template
        return get_template(template).render(Context(context))


