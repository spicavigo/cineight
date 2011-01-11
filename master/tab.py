from django.utils.datastructures import SortedDict
from django.http import HttpResponse
from utils.json_utils import JsonResponse
from django.conf import settings
from django.db.models import Avg, Max, Min, Count
import ast
import urllib2
from utils.tab import Tab
from master import element as E
from master import models as M
from utils.nodes import Node
from utils.callback import Callback
from master import data_methods as dm
cb = Callback()

def escape(q):
    if not q: return q
    li = ['+','-','&&','||','!','(',')','{', '}', '[', ']', '^', '"', '~', '*', '?', ':', '\\']
    q = ''.join(map(lambda e: e in li and ' ' or e, q))
    return q

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
        query_dict = {'query':escape(self.client) or '*'}
        query_url = '_val_:"scale(log(sum(votes,1)),0,10)"^10 name:(%(query)s)^5 name:"%(query)s"^10 alternative_name:(%(query)s)^3 alternative_name:"%(query)s"^3 original_name:(%(query)s)^3 original_name:"%(query)s"^3' % query_dict
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

class SuggestionTab(Tab):
    _element_class = E.SearchResultUserElement
    title = 'Leaders'
    
    def _prepare(self):
        recs = sorted(M.Reco.objects.filter(user_to=1).values('user_from').annotate(count=Count('user_from')), key=lambda rec: rec['count'], reverse=True)
        self.ids=[]
        follows = [item for e in  self.user.follow.values_list('id') for item in e] + [self.user.id, 1, 19]
        count = 0
        for e in recs:
            if not e['user_from'] in follows:
                self.ids.append(M.UserProfile.objects.get(id=e['user_from']))
                count += 1
                if count == 3:break

class FriendSuggestionTab(Tab):
    _element_class = E.SearchResultUserElement
    title = 'FB Friends'
    
    def _prepare(self):
        friends = dm.get_fb_friends(self.client)
        following = [e.user.username for e in self.user.follow.all()]
        self.ids = M.User.objects.filter(username__in = list(set(friends) - set(following)))[:3]
        self.ids = [e.userprofile for e in self.ids]
        
    
class ListListTab(Tab):
    _element_class = E.ListListElement
    title = 'Public Lists'
    
    def _prepare(self):
        self.ids = M.List.objects.all()
    
    def show(self, *args, **kwargs):
        return super(ListListTab, self).show(count = len(self.ids))

class ListTab(Tab):
    _element_class = E.ListElement
    title = 'All'
    
    def _prepare(self):
        self.ids = M.PublicList.objects.filter(list=self.client).order_by('pos')
        self.context['title'] =self.client.name
    

class ListSeenTab(Tab):
    _element_class = E.ListElement
    title = 'Seen \'Em'
    
    def _prepare(self):
        movies = M.PublicList.objects.filter(list=self.client)        
        self.ids = M.UserMovieList.objects.filter(movie__in = [e.movie.id for e in movies], user = self.user, list = 'SL').order_by('-timestamp')
        self.context['desc'] = 'Movies that you have seen in <b>%s</b> list' % self.client.name
        self.context['id'] = 'SL'
        self.context['title'] = 'Seen \'Em (%d/%d)' % (len(self.ids), len(movies))


class ListUnSeenTab(Tab):
    _element_class = E.ListElement
    title = 'To Watch'
    
    def _prepare(self):
        movies = M.PublicList.objects.filter(list=self.client)        
        self.ids = M.UserMovieList.objects.filter(movie__in = [e.movie.id for e in movies], user = self.user, list = 'WL').order_by('-timestamp')
        self.context['desc'] = 'Movies that you want to watch in <b>%s</b> list' % self.client.name
        self.context['id'] = 'WL'
        self.context['title'] = 'To Watch (%d/%d)' % (len(self.ids), len(movies))
    

class ListFilterTab(Tab):
    _element_class = E.ListElement
    title = 'Trash'
    
    def _prepare(self):
        movies = M.PublicList.objects.filter(list=self.client)        
        self.ids = M.UserMovieList.objects.filter(movie__in = [e.movie.id for e in movies], user = self.user, list = 'FL').order_by('-timestamp')
        self.context['desc'] = 'Movies that you do not like in <b>%s</b> list' % self.client.name
        self.context['id'] = 'FL'
        self.context['title'] = 'Trash (%d/%d)' % (len(self.ids), len(movies))
    

class RollTab(Tab):
    _element_class = E.ListElement
    title = 'Roll'
    
    def _prepare(self):
        self.ids = []
        t1 = AskRecoTab(user=self.user, is_default=True, tab_client=None)
        t2 = UpdateTab(user=self.user, is_default=True, tab_client=None)
        self.context['updates'] = t2.show()
        self.context['asks'] = t1.show()
        
class AskRecoTab(Tab):
    _element_class = E.AskRecoElement
    title = ''
    
    def _prepare(self):
        self.ids = M.AskReco.objects.filter(user_to=self.user).order_by('-timestamp')
        
class UpdateTab(Tab):
    _element_class = E.UpdateElement
    title = 'Updates'
    
    def _prepare(self):
        self.ids = M.Activity.objects.filter(user__in=[e.id for e in self.user.follow.all()]).order_by('-timestamp')
    
    def show(self, is_json=False, start=0, count=10):
        #self.context['title'] = Node(self.title, data_id=self.get_data.key)
        r= super(UpdateTab, self).show(None, is_json, start, count,
                next_key = '%s+%s' % (self.get_next.key, self.client or ''),
                prev_key = '%s+%s' % (self.get_next.key, self.client or ''))
        return r

    @staticmethod
    @cb.register
    def get_next(request):
        data_id = request.GET.get('data_id').split('+')[1:]
        start = int(data_id[1])
        query = data_id[0]
        return HttpResponse(UpdateTab(request.user.userprofile, True, query).show(start=start)['html'])