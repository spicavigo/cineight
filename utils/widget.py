#!/usr/bin/env python
#
#       widget.py
#       

import re
from utils.container import Container
from utils import data_methods as dm
url_names = ['professor_prof_page',
             'professor_landing_page',
             'professor_course_page',
             'restaurant_menu_page',
             'partner_restaurant_form_page',
             'housing_landing_page',
             'housing_search_page',
             'home_page',
             'rest_menu_form',
             'professor_pc_page',
             'restaurant_landing_page',
             'job_search_page',
             'course_page',
             'prof_home_page',
             'ajax_url',
             'company_page',
             'property_page',             
             'master_home_page',
             'job_redirect_page',
             'prof_search_page',
             'master_prelogin_page',
             'master_authentication_page',
             'master_setting_page',
             'master_userinfo_page',
             'master_logout_page',
             'partner_restaurant_circle_page',
             'partner_restaurant_home_page',
             'partner_restaurant_menu_form_page',
             'partner_restaurant_circle_page',
             'master_validation_page',
             'restaurant_search_page',
             'restaurant_prelogin_page',
             'partner_restaurant_login_page',
             'partner_upload_menu_page',
             'partner_restaurant_logout_page',
             'facade_professor_page',
             'facade_course_page',
             'facade_profcourse_page',
             'facade_job_page',
             'facade_housing_page',
             'facade_restaurant_page',
             'master_alt_signup_page',
             'error_404_page',
             'error_500_page',
             'master_facade_page',
             'job_detail_page',
             'housing_detail_page',
             'facade_browse_page',
             'facade_browse_module_page',
             'facade_browse_course_page',
             'facade_course_course_page',
             'facade_course_professor_page',
             'facade_course_pc_page',
             'facade_browse_job_page',
             'facade_browse_housing_page',
             'facade_browse_restaurant_page',
             'restaurant_payment_response_page',
             'master_movie_page',
             'master_user_page',
             'master_search_page',
             'master_landing_page',
             'master_list_landing',
             ]


class WidgetMeta(type):
    def __init__(cls, name, bases, dict):
        for b in bases:
            if hasattr(b, '_registry'):
                pat = re.compile(dict['urlpat'])                
                urls = [e for e in b._registry.keys() if re.search(pat, e)]
                for e in urls:b._registry[e].append((dict['index'], cls))
                cls.widget_id = name
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

class Widget(Container):
    __metaclass__ = WidgetMeta
    _registry = dict([(e,[]) for e in url_names])    
    title = "Widget"

    def __init__(self, *args, **kwargs):
        excludes = dm.get_excludes(args[0].user)
        self.tabs = filter(lambda x: x.__module__ + '.' + x.__name__ not in excludes and x.__module__ not in excludes, self._tab_class)
        
        self.tabs = map(lambda x, i: x(user = getattr(self, 'user', args[0].user),
                            is_default = getattr(self, 'default_tab', i)==i,
                            tab_client = getattr(self, 'client', None)
                            ), self.tabs, range(len(self.tabs))
                        )
         
        self.context = {'tabs': [], 'id': self.widget_id, 'title' : self.title,'images': self._media.images}
        self.request = None

    def show(self, template = None, is_json = False, start = 0, count = 10):
        if len(self.context['tabs'])==0 :
            self.context['tabs'] = [t.show(start = start, count = count, is_json = is_json) for t in self.tabs]
        return super(Widget, self).show(template, self.context, is_json)

    @classmethod
    def get_css(cls):
        return cls._media.css + cls._media.extra_css

    @classmethod
    def get_js(cls):
        return cls._media.js + cls._media.extra_js
