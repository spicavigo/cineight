from django.utils.datastructures import SortedDict
from django.http import HttpResponse
from utils.json_utils import JsonResponse
from django.conf import settings
import ast
import urllib2
from utils.tab import Tab
from master import element as E
from master import models as M
from utils.nodes import Node
from utils.callback import Callback
cb = Callback()

class HeaderTab(Tab):
    _element_class = E.HeaderElement
    title = ''

class LoginTab(Tab):
    _element_class = E.LoginElement
    title = 'Login'

class SignUpTab(Tab):
    _element_class = E.SignUpElement
    title = ''
    
class ForwardRecoTab(Tab):
    _element_class = E.RecoElement
    title = 'My Recommendations'
    
    def _prepare(self):
        self.ids = SortedDict([(e.movie, e) for e in M.Reco.objects.select_related('movie').filter(user_from=self.client).order_by('-timestamp')]).values()
        self.context['desc'] = 'Movies that you recommend to your followers'
        self.context['id'] = 'FR'
        
    def show(self, is_json=False, start=0, count=10):
        #self.context['title'] = Node(self.title, data_id=self.get_data.key)
        r= super(ForwardRecoTab, self).show(None, is_json, start, count,
                next_key = '%s+%s' % (self.get_next.key, self.client.id),
                prev_key = '%s+%s' % (self.get_next.key, self.client.id))
        return r

    @staticmethod
    @cb.register
    def get_next(request):
        data_id = request.GET.get('data_id').split('+')[1:]
        start = int(data_id[1])
        user = M.UserProfile.objects.get(id=data_id[0])
        return HttpResponse(ForwardRecoTab(request.user.userprofile, True, user).show(start=start)['html'])

class ReverseRecoTab(Tab):
    _element_class = E.RecoElement
    title = 'Recommendations to Me'
    
    def _prepare(self):
        self.ids = M.Reco.objects.select_related('movie').filter(user_to=self.client).order_by('-timestamp')
        self.context['desc'] = 'Movies recommended to you, by users you follow'
        self.context['id'] = 'RR'
    
    
    def show(self, is_json=False, start=0, count=10):
        #self.context['title'] = Node(self.title, data_id=self.get_data.key)
        r= super(ReverseRecoTab, self).show(None, is_json, start, count,
                next_key = '%s+%s' % (self.get_next.key, self.client.id),
                prev_key = '%s+%s' % (self.get_next.key, self.client.id))
        return r

    @staticmethod
    @cb.register
    def get_next(request):
        data_id = request.GET.get('data_id').split('+')[1:]
        start = int(data_id[1])
        user = M.UserProfile.objects.get(id=data_id[0])
        return HttpResponse(ReverseRecoTab(request.user.userprofile, True, user).show(start=start)['html'])


class SeenListTab(Tab):
    _element_class = E.ListElement
    title = 'To Watch'
    
    def _prepare(self):
        self.ids = M.UserMovieList.objects.select_related('movie').filter(user = self.client, list = 'WL').order_by('-timestamp')
        self.context['desc'] = 'Movies that you want to watch'
        self.context['id'] = 'WL'
    
    def show(self, is_json=False, start=0, count=10):
        #self.context['title'] = Node(self.title, data_id=self.get_data.key)
        r= super(SeenListTab, self).show(None, is_json, start, count,
                next_key = '%s+%s' % (self.get_next.key, self.client.id),
                prev_key = '%s+%s' % (self.get_next.key, self.client.id))
        return r

    @staticmethod
    @cb.register
    def get_next(request):
        data_id = request.GET.get('data_id').split('+')[1:]
        start = int(data_id[1])
        user = M.UserProfile.objects.get(id=data_id[0])
        return HttpResponse(SeenListTab(request.user.userprofile, True, user).show(start=start)['html'])

class UnseenListTab(Tab):
    _element_class = E.ListElement
    title = "Seen 'Em"
    
    def _prepare(self):
        self.ids = M.UserMovieList.objects.select_related('movie').filter(user = self.client, list = 'SL').order_by('-timestamp')
        self.context['desc'] = 'Movies that you have watched (including the ones you recommend)'
        self.context['id'] = 'SL'
    
    def show(self, is_json=False, start=0, count=10):
        #self.context['title'] = Node(self.title, data_id=self.get_data.key)
        r= super(UnseenListTab, self).show(None, is_json, start, count,
                next_key = '%s+%s' % (self.get_next.key, self.client.id),
                prev_key = '%s+%s' % (self.get_next.key, self.client.id))
        return r

    @staticmethod
    @cb.register
    def get_next(request):
        data_id = request.GET.get('data_id').split('+')[1:]
        start = int(data_id[1])
        user = M.UserProfile.objects.get(id=data_id[0])
        return HttpResponse(UnseenListTab(request.user.userprofile, True, user).show(start=start)['html'])

class FilterListTab(Tab):
    _element_class = E.ListElement
    title = 'Trash Can'
    
    def _prepare(self):
        self.ids = M.UserMovieList.objects.select_related('movie').filter(user = self.client, list = 'FL').order_by('-timestamp')
        self.context['desc'] = 'Movies you don\'t wish to watch'
        self.context['id'] = 'FL'
    
    def show(self, is_json=False, start=0, count=10):
        #self.context['title'] = Node(self.title, data_id=self.get_data.key)
        r= super(FilterListTab, self).show(None, is_json, start, count,
                next_key = '%s+%s' % (self.get_next.key, self.client.id),
                prev_key = '%s+%s' % (self.get_next.key, self.client.id))
        return r

    @staticmethod
    @cb.register
    def get_next(request):
        data_id = request.GET.get('data_id').split('+')[1:]
        start = int(data_id[1])
        user = M.UserProfile.objects.get(id=data_id[0])
        return HttpResponse(FilterListTab(request.user.userprofile, True, user).show(start=start)['html'])
        
class MovieDetailTab(Tab):
    _element_class = E.MovieDetailElement
    title = ''
    
class RecommenderTab(Tab):
    _element_class = E.RecommenderElement
    title = 'Recommended By'
    
    def _prepare(self):
        self.ids = SortedDict([(e.user, e) for e in M.MovieRating.objects.select_related('movie').filter(movie=self.client, rating__gt=0)]).values()
        #self.ids = M.Reco.objects.filter(movie=self.client)

class WarnerTab(Tab):
    _element_class = E.RecommenderElement
    title = 'Warned By'
    
    def _prepare(self):
        self.ids = SortedDict([(e.user, e) for e in M.MovieRating.objects.select_related('movie').filter(movie=self.client, rating__lt=0)]).values()
        
class ReviewTab(Tab):
    _element_class = E.ReviewElement
    title = ''
    
    def _prepare(self):
        self.ids = M.MovieReview.objects.filter(movie=self.client).order_by('-timestamp')

class UserTab(Tab):
    _element_class = E.UserElement
    title=''
    
class SearchTab(Tab):
    _element_class = E.SearchElement
    title=''

class SearchResultTab(Tab):
    _element_class = E.SearchResultElement
    title='Movies'
    
    def _prepare(self):
        query_dict = {'query':self.client or '*'}
        query_url = '_val_:"scale(log(sum(votes,1)),0,10)"^10 name:(%(query)s)^5 name:"%(query)s"^5 alternative_name:(%(query)s)^3 alternative_name:"%(query)s"^3 original_name:(%(query)s)^3 original_name:"%(query)s"^3' % query_dict
        query_url = urllib2.quote(query_url)
        static_url = settings.SOLR_URL + 'q=%s&version=2.2&wt=python&rows=100&start=0&qt=standard&fl=*,score'
        conn = urllib2.urlopen(static_url % query_url)
        rsp = ast.literal_eval(conn.read())    
        result = [e for e in rsp['response']['docs']]
        
        #self.ids = M.Movie.objects.filter(name__icontains=self.client or '')
        self.ids = [M.Movie.objects.get(id=e['id']) for e in result]
        
    
    def show(self, is_json=False, start=0, count=10):
        #self.context['title'] = Node(self.title, data_id=self.get_data.key)
        r= super(SearchResultTab, self).show(None, is_json, start, count,
                next_key = '%s+%s' % (self.get_next.key, self.client or ''),
                prev_key = '%s+%s' % (self.get_next.key, self.client or ''))
        return r

    @staticmethod
    @cb.register
    def get_next(request):
        data_id = request.GET.get('data_id').split('+')[1:]
        start = int(data_id[1])
        query = data_id[0]
        return HttpResponse(SearchResultTab(request.user.userprofile, True, query).show(start=start)['html'])

class SearchResultUserTab(Tab):
    _element_class = E.SearchResultUserElement
    title = 'Users'
    
    def _prepare(self):
        self.ids = M.UserProfile.objects.filter(user__username__icontains=self.client or '')
    
    def show(self, is_json=False, start=0, count=10):
        #self.context['title'] = Node(self.title, data_id=self.get_data.key)
        r= super(SearchResultUserTab, self).show(None, is_json, start, count,
                next_key = '%s+%s' % (self.get_next.key, self.client or ''),
                prev_key = '%s+%s' % (self.get_next.key, self.client or ''))
        return r

    @staticmethod
    @cb.register
    def get_next(request):
        data_id = request.GET.get('data_id').split('+')[1:]
        start = int(data_id[1])
        query = data_id[0]
        return HttpResponse(SearchResultUserTab(request.user.userprofile, True, query).show(start=start)['html'])

class FeedbackTab(Tab):
    _element_class = E.FeedbackElement
    title = 'Feedback'