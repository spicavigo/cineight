from django.conf.urls.defaults import *
import settings
from django.contrib.auth.views import login, logout_then_login, logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from master import page as mpage

urlpatterns = patterns('',
    # Example:
    # (r'^reco/', include('reco.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^accounts/', include('socialauth.urls')),
    #(r'^$', 'socialauth.views.signin_complete'),
    (r'^admin/(.*)', admin.site.root),
    (r'^util/', include('utils.urls')),
    
    url(r'^logout$', logout, {'next_page': '/'}),
    url(r'^$', mpage.LandingPage(), name='master_landing_page'),
    url(r'^home$', mpage.HomePage(), name = 'master_home_page'),
    url(r'^movie/(?P<movie>\d+)/.*?$', mpage.MoviePage(), name='master_movie_page'),
    url(r'^user/(?P<user>\d+)/.*?$', mpage.UserPage(), name='master_user_page'),
    url(r'^search$', mpage.SearchPage(), name = 'master_search_page'),
)
urlpatterns += patterns("django.views",
        url(r"%s(?P<path>.*)/$" % settings.MEDIA_URL[1:], "static.serve", {
            "document_root": settings.MEDIA_ROOT,
        })
    )