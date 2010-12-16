#!/usr/bin/env python
#
#       element.py
#       
from utils.container import Container

class ElementMeta(type):
    def __init__(cls, name, bases, dict):
        for b in bases:
            if hasattr(b, '_registry'):
                module = __import__(dict['__module__'].rsplit('.',1)[0]+'.media', fromlist=[dict['__module__'].rsplit('.',1)[0]])
                try:
                    cls._media = getattr(module, name+'Media')()
                except AttributeError:
                    cls._media = getattr(module, 'DefaultMedia')()                
                cls._media.css=[e.startswith('http') and e or cls._media.css_prefix+e for e in cls._media.css]
                cls._media.js=[e.startswith('http') and e or cls._media.js_prefix+e for e in cls._media.js]                
                #cls._media.template = get_template(cls._media.template)
                break      
        return type.__init__(cls, name, bases, dict)
        
class Element(Container):
    __metaclass__ = ElementMeta
    _registry = {}
    def __init__(self, user, client):
        self.client = client
        self.user = user
        self._prepare()

    def _prepare(self):
        pass

    def show(self, template = None, context = None, is_json = False):
        context = context or self.context
        if type(context) == type({}):
            context['images'] = self._media.images
        return super(Element, self).show(template, context, is_json)
