#!/usr/bin/env python
from django.http import HttpResponseRedirect
from utils.page import DefaultPage
from utils.page import Page

from django.contrib.auth.models import User

from master import box as B

class LandingPage(Page):
    url = 'master_landing_page',
    template = 'master/PageLanding.html'
    
    def __init__(self):
        self.header = B.HeaderBox
        self.boxes = [B.LoginBox, B.SignUpBox]
        super(LandingPage, self).__init__(login_required=False)
    
    def view(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home')
        return super(LandingPage, self).show(request)
        
class HomePage(Page):
    url = 'master_home_page'
    template = 'master/PageMain.html'
    
    def __init__(self):
        self.header = B.HeaderBox
        self.boxes = [B.SearchBox, B.RecoBox, B.UserBox, B.CompareBox, B.FeedbackBox]
        super(HomePage, self).__init__(login_required=True)
        
    def view(self, request):
        return super(HomePage, self).show(request)
        
class MoviePage(Page):
    url = 'master_movie_page'
    template = 'master/PageMovie.html'
    
    def __init__(self):
        self.header = B.HeaderBox
        self.boxes = [B.SearchBox, B.MovieDetailBox, B.RecommenderBox, B.ReviewBox, B.CompareBox, B.FeedbackBox]
        super(MoviePage, self).__init__(login_required=True)
        
    def view(self, request, *args, **kwargs):
        return super(MoviePage, self).show(request, *args, **kwargs)
        
class UserPage(Page):
    url = 'master_user_page'
    template = 'master/PageMain.html'
    
    def __init__(self):
        self.header = B.HeaderBox
        self.boxes = [B.SearchBox, B.UserRecoBox, B.UserBox, B.CompareBox, B.FeedbackBox]
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