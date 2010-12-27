
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

from utils.box import Box
from master import tab as T
from master import models as M

from utils.json_utils import JsonResponse
import json
from utils.callback import Callback
cb = Callback()

class HeaderBox(Box):
    _tab_class = [T.HeaderTab]
    title = ''

class LoginBox(Box):
    _tab_class = [T.LoginTab]
    title = ''

class SignUpBox(Box):
    _tab_class = [T.SignUpTab]
    title = ''

class RecoBox(Box):
    _tab_class = [T.ReverseRecoTab, T.ForwardRecoTab, T.SeenListTab, T.UnseenListTab, T.FilterListTab]
    title=''
    
    def __init__(self, request, * args, ** kwargs):
        self.client = request.user.userprofile
        self.user = self.client
        super(RecoBox, self).__init__(request, * args, ** kwargs)
    
#class ListBox(Box):
#    _tab_class = [T.SeenListTab, T.UnseenListTab, T.FilterListTab]
#    title = ''

class UserRecoBox(Box):
    _tab_class = [T.ForwardRecoTab, T.SeenListTab, T.UnseenListTab, T.FilterListTab]
    title=''
    
    def __init__(self, request, * args, ** kwargs):
        self.client = M.UserProfile.objects.get(id=kwargs.get('user'))
        self.user = request.user.userprofile
        super(UserRecoBox, self).__init__(request, * args, ** kwargs)
    
class MovieDetailBox(Box):
    _tab_class = [T.MovieDetailTab]
    title = ''
    
    def __init__(self, request, * args, ** kwargs):
        self.client = M.Movie.objects.get(id=kwargs.get('movie'))
        self.user = request.user.userprofile
        super(MovieDetailBox, self).__init__(request, * args, ** kwargs)
    
class RecommenderBox(Box):
    _tab_class=[T.RecommenderTab, T.WarnerTab]
    title=''
    
    def __init__(self, request, * args, ** kwargs):
        self.client = M.Movie.objects.get(id=kwargs.get('movie'))
        self.user = request.user.userprofile
        super(RecommenderBox, self).__init__(request, * args, ** kwargs)
        
class ReviewBox(Box):
    _tab_class=[T.ReviewTab]
    title = ''
    
    def __init__(self, request, * args, ** kwargs):
        self.client = M.Movie.objects.get(id=kwargs.get('movie'))
        self.user = request.user.userprofile
        super(ReviewBox, self).__init__(request, * args, ** kwargs)
        

class CompareBox(Box):
    _tab_class=[]
    title=''
    
    def __init__(self, request, * args, ** kwargs):
        self.user = request.user.userprofile
        super(CompareBox, self).__init__(request, * args, ** kwargs)
        self.context['get_data'] = self.get_cl_data.key
        
    @staticmethod
    @cb.register
    def get_cl_data(request):
        movies = [e.movie for e in M.UserMovieList.objects.select_related('movie').filter(user=request.user.userprofile, list='CL')]
        t=get_template('master/ElementCompare.html').render(Context({'movies':movies, 'purge': CompareBox.purge.key}))
        #return JsonResponse(json.dumps(cls))
        return HttpResponse(t)
    
    @staticmethod
    @cb.register
    def purge(request):
        user = request.user.userprofile
        M.UserMovieList.objects.filter(user=user, list='CL').delete()
        return HttpResponse('ok')
        
class UserBox(Box):
    _tab_class=[T.UserTab]
    title=''
    
    def __init__(self, request, * args, ** kwargs):
        self.user = request.user.userprofile
        id = kwargs.get('user')
        if id:
            self.client = M.UserProfile.objects.get(id=id)
        else:
            self.client = request.user.userprofile
        super(UserBox, self).__init__(request, * args, ** kwargs)
        
class SearchBox(Box):
    _tab_class = [T.SearchTab]
    title=''
    
    def __init__(self, request, * args, ** kwargs):
        self.client = request.POST.get('q')
        self.user = request.user.userprofile
        super(SearchBox, self).__init__(request, * args, ** kwargs)

class SearchResultBox(Box):
    _tab_class = [T.SearchResultTab, T.SearchResultUserTab]
    title=''
    
    def __init__(self, request, * args, ** kwargs):
        self.client = request.POST.get('q')
        self.user = request.user.userprofile
        super(SearchResultBox, self).__init__(request, * args, ** kwargs)

class FeedbackBox(Box):
    _tab_class = [T.FeedbackTab]
    title = ''
    
    def __init__(self, request, * args, ** kwargs):
        self.user = request.user.userprofile
        super(FeedbackBox, self).__init__(request, * args, ** kwargs)

class SuggestionBox(Box):
    _tab_class = [T.SuggestionTab]
    
    def __init__(self, request, * args, ** kwargs):
        self.user = request.user.userprofile
        super(SuggestionBox, self).__init__(request, * args, ** kwargs)

class ListListBox(Box):
    _tab_class = [T.ListListTab]
    title = 'Public Lists'
    
    def __init__(self, request, * args, ** kwargs):
        self.user = request.user.userprofile
        super(ListListBox, self).__init__(request, * args, ** kwargs)

class ListBox(Box):
    _tab_class = [T.ListTab, T.ListSeenTab, T.ListUnSeenTab, T.ListFilterTab]
    title = ''
    
    def __init__(self, request, * args, ** kwargs):
        self.user = request.user.userprofile
        self.client = M.List.objects.get(id=kwargs.get('list_name'))
        super(ListBox, self).__init__(request, * args, ** kwargs)