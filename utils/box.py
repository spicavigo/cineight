#!/usr/bin/env python
#
#       box.py
#       
import json
from django.template.loader import get_template
from utils.container import Container
from utils import data_methods as dm

class BoxMeta(type):
    def __init__(cls, name, bases, dict):
        for b in bases:
            if hasattr(b, '_registry'):
                b._registry[name] = cls
                cls.box_id = name
                module = __import__(dict['__module__'].rsplit('.',1)[0]+'.media', fromlist=[dict['__module__'].rsplit('.',1)[0]])
                try:
                    cls._media = getattr(module, name+'Media')()
                except AttributeError:
                    cls._media = getattr(module, 'DefaultMedia')()
                cls._media.css = [e.startswith('http') and e or cls._media.css_prefix+e for e in cls._media.css]
                cls._media.js = [e.startswith('http') and e or cls._media.js_prefix+e for e in cls._media.js]
                for elem in dict['_tab_class']:
                    cls._media.extra_css = cls._media.extra_css + elem._media.css + elem._media.extra_css
                    cls._media.extra_js = cls._media.extra_js + elem._media.js + elem._media.extra_js
                #cls._media.template = get_template(cls._media.template)
                break
        return type.__init__(cls, name, bases, dict)
        
class Box(Container):
    __metaclass__ = BoxMeta
    _registry = {}
    title = "Box"
        
    def __init__(self, *args, **kwargs):
        excludes = dm.get_excludes(args[0].user)
        self.tabs = filter(lambda x: x.__module__ + '.' + x.__name__ not in excludes and x.__module__ not in excludes, self._tab_class)
        self.tabs = map(lambda x, i: x(user = getattr(self, 'user', args[0].user),
                            is_default = getattr(self, 'default_tab', i)==i,
                            tab_client = getattr(self, 'client', None)
                            ), self.tabs, range(len(self.tabs))
                        )
         
        self.context = {'tabs': [], 'id': self.box_id, 'title' : self.title,
                        'tab_style': getattr(self, 'tab_style', 'horizontal'),
                        'images': self._media.images}
        self.request = None

    def show(self, template = None, is_json = False, start = 0, count = 10):
        self.context['tabs'] = [t.show(start = start, count = count, is_json = is_json) for t in self.tabs]
        return super(Box, self).show(template, self.context, is_json)

    @classmethod
    def get_css(cls):
        return cls._media.css + cls._media.extra_css

    @classmethod
    def get_js(cls):
        return cls._media.js + cls._media.extra_js


        
