#!/usr/bin/env python
from django.http import HttpResponseRedirect
from utils.page import DefaultPage
from utils.page import Page

from django.contrib.auth.models import User
from django.conf import settings
from master import box as B
from master import data_methods as dm
from master import models as M
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
import urllib

class LandingPage(Page):
    url = 'master_landing_page',
    template = 'master/PageLanding.html'
    
    def __init__(self):
        self.header = B.HeaderBox
        self.boxes = [B.LoginBox, ]#B.SignUpBox]
        super(LandingPage, self).__init__(login_required=False)
    
    def view(self, request):
        self.context['FB_REDIRECT'] = False
        user = None

        if request.GET.get('signed_request'):
            data = dm.parse_signed_request(request.GET.get('signed_request'))
            #if not data or not data.get('user_id'):
            args = dict(client_id=settings.FACEBOOK_APP_ID, redirect_uri='http://apps.facebook.com/cineight/', scope  = ','.join(settings.FACEBOOK_EXTENDED_PERMISSIONS))#,type='user_agent', display='popup')
            self.context['FB_URL'] = "https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(args)
            self.context['FB_REDIRECT'] = True

            #else:
            #    user = authenticate(username=data['user_id'], password='')
                
                #return HttpResponseRedirect(self.context['FB_URL'])
        if request.GET.get('code'):
            user = authenticate(request=request)

        if user:
            login(request, user)
        if request.user.is_authenticated():
            user = request.user
            if user.authmeta_set.filter(provider='Facebook').count():
                #1. get movies from FB profile
                #2. Convert them to CE
                #3. Call recommend for each
                movies = dm.get_fb_movies(request)
                [dm.recommend(user.userprofile, M.Movie.objects.get(id=e)) for e in movies]
            return HttpResponseRedirect('/home')
        return super(LandingPage, self).show(request)
        
class HomePage(Page):
    url = 'master_home_page'
    template = 'master/PageMain.html'
    
    def __init__(self):
        self.header = B.HeaderBox
        self.boxes = [B.SearchBox, B.RecoBox, B.UserBox, B.CompareBox, B.FeedbackBox, B.SuggestionBox]
        super(HomePage, self).__init__(login_required=True)
        
    def view(self, request):
        return super(HomePage, self).show(request)
        
class MoviePage(Page):
    url = 'master_movie_page'
    template = 'master/PageMovie.html'
    
    def __init__(self):
        self.header = B.HeaderBox
        self.boxes = [B.SearchBox, B.MovieDetailBox, B.RecommenderBox, B.ReviewBox, B.CompareBox, B.FeedbackBox]
        super(MoviePage, self).__init__(login_required=False)
        
    def __call__(self,request,*args,**kwargs):
        if isinstance(request.user, AnonymousUser):
            self.boxes = [B.MovieDetailBox,]
        else:
            self.boxes = [B.SearchBox, B.MovieDetailBox, B.RecommenderBox, B.ReviewBox, B.CompareBox, B.FeedbackBox]
        return super(MoviePage, self).__call__(request, *args, **kwargs)
        
    def view(self, request, *args, **kwargs):
        self.context['movie'] = M.Movie.objects.get(id=kwargs.get('movie'))
        return super(MoviePage, self).show(request, *args, **kwargs)
        
class UserPage(Page):
    url = 'master_user_page'
    template = 'master/PageMain.html'
    
    def __init__(self):
        self.header = B.HeaderBox
        self.boxes = [B.SearchBox, B.UserRecoBox, B.UserBox, B.CompareBox, B.FeedbackBox, B.SuggestionBox]
        super(UserPage, self).__init__(login_required=True)
        
    def view(self, request, *args, **kwargs):
        return super(UserPage, self).show(request, *args, **kwargs)
        
class SearchPage(Page):
    url='master_search_page'
    template = 'master/PageMain.html'
    
    def __init__(self):
        self.header = B.HeaderBox
        self.boxes = [B.SearchBox, B.SearchResultBox, B.CompareBox, B.FeedbackBox]
        super(SearchPage, self).__init__(login_required=True)
        
    def view(self, request, *args, **kwargs):
        return super(SearchPage, self).show(request, *args, **kwargs)

class ListLandingPage(Page):
    url = 'master_list_landing'
    template = 'master/PageMain.html'
    
    def __init__(self):
        self.header = B.HeaderBox
        self.boxes = [B.SearchBox, B.ListListBox, B.UserBox, B.CompareBox, B.FeedbackBox, B.SuggestionBox]
        super(ListLandingPage, self).__init__(login_required=True)
        
    def view(self, request, *args, **kwargs):
        return super(ListLandingPage, self).show(request, *args, **kwargs)

class ListPage(Page):
    url = 'master_list_page'
    template = 'master/PageMain.html'
    
    def __init__(self):
        self.header = B.HeaderBox
        self.boxes = [B.SearchBox, B.ListBox, B.UserBox, B.CompareBox, B.FeedbackBox, B.SuggestionBox]
        super(ListPage, self).__init__(login_required=True)
        
    def view(self, request, *args, **kwargs):
        return super(ListPage, self).show(request, *args, **kwargs)