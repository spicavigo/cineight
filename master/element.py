from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.forms.fields import email_re
from django.http import HttpResponse
from django.conf import settings
from utils.json_utils import JsonResponse
from master import models as M
from master import data_methods as dm
import json
import xmlrpclib
import time
import ast
import urllib2
from utils.element import Element
from utils.callback import Callback
cb = Callback()
SERVER = s = xmlrpclib.Server('http://localhost:7777/', allow_none=True)

def escape(q):
    if not q: return q
    li = ['+','-','&&','||','!','(',')','{', '}', '[', ']', '^', '"', '~', '*', '?', ':', '\\']
    q = ''.join(map(lambda e: e in li and ' ' or e, q))
    return q

def _add_to_list(user, movie, li):
    if li=='CL':
        obj, created = M.UserMovieList.objects.get_or_create(user=user, movie=movie, list=li)
        if not created:obj.delete()
        return 
    movis = M.UserMovieList.objects.filter(user=user, movie = movie)
    for m in movis:
        if not m.list == 'CL':
            if m.list == li:
                try:
                    SERVER.removed(m.id)
                except:pass
                m.delete()
                return
            try:
                SERVER.removed(m.id)
            except:pass
            m.list = li
            m.save()
            try:
                SERVER.added(m.id)
            except:pass
            return
    m = M.UserMovieList.objects.create(user=user, movie=movie, list=li)
    try:
        SERVER.added(m.id)
    except:pass
    
@cb.register
def recommend(request):
    movie = request.GET.get('data_id').split('+')[1]
    user = request.user.userprofile
    movie=M.Movie.objects.get(id=movie)
    followers = user.follower.all()
    comment = request.GET.get('comment')[:254]
    obj, created = M.Reco.objects.get_or_create(user_from=user, user_to=M.UserProfile.objects.get(id=1), movie = movie, defaults = {'comment':comment})
    obj.comment = comment
    obj.save()
    
    rating = int(request.GET.get('rating'))
    robj, rcreated = M.MovieRating.objects.get_or_create(user=user, movie=movie, defaults={'rating':rating})
    robj.rating = rating
    robj.save()
    
    if created:
        try:
            SERVER.reco_add(user.id, obj.id)
        except:pass
        
    for f in followers:
        obj, created = M.Reco.objects.get_or_create(user_from=user, user_to=f, movie = movie, defaults = {'comment':comment})
        obj.comment = comment
        obj.save()
        if created:
            try:
                SERVER.reco_add(f.id, obj.id)
            except:pass
    
    obj, created = M.MovieReview.objects.get_or_create(user=user, movie=movie, defaults={'review': comment})
    obj.review = comment
    obj.save()
    li = rating > 0 and 'SL' or 'FL'
    if not M.UserMovieList.objects.filter(user=user, movie=movie, list=li).count():
        _add_to_list(user, movie, li)
    
    dm.tweet(movie, rating)
    from master.tab import ReviewTab
    return HttpResponse(ReviewTab(user, True, tab_client=movie).show()['html'])
    
@cb.register
def add_to_list(request):
    movie, li = request.GET.get('data_id').split('+')[1:]
    movie=M.Movie.objects.get(id=movie)
    user = request.user.userprofile
    _add_to_list(user, movie, li)
    return HttpResponse('ok')          

@cb.register
def follow(request):
    peer = request.GET.get('data_id').split('+')[1]
    user = request.user.userprofile
    peer = M.UserProfile.objects.get(id=peer)
    if peer in user.follow.all():
        user.follow.remove(peer)
        peer.follower.remove(user)
        M.Reco.objects.filter(user_from=peer, user_to=user).delete()
        response = 'Follow'
    else:
        user.follow.add(peer)
        peer.follower.add(user)
        recs = M.Reco.objects.filter(user_from=peer)
        temp={}
        for e in recs:
            try:
                temp[e.movie.id] = e
            except:pass
        for k,v in temp.items():
            r = M.Reco.objects.create(user_from=peer, user_to=user, movie=v.movie, comment=v.comment)
            r.timestamp = v.timestamp
            r.save()
        response = 'Stop Following'
    user.save()
    return HttpResponse(response)

class HeaderElement(Element):
    def _prepare(self):
        self.context = {'user': self.user.is_authenticated(),
                        'lists': M.List.objects.all()[:5],}
        print M.List.objects.all()[:5]

class LoginElement(Element):
    def _prepare(self):
        self.context ={
            'data_id': self.login.key,
            'ts': time.time()
        }
    
    @staticmethod
    @cb.register
    def login(request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        error = ''
        success = True
        user = authenticate(username=username, password=password)
        if not user:
            error = 'Invalid Email or password'
            success = False
        else:
            login(request, user)
        print json.dumps({'success': success, 'url': '/home', 'error': error})
        return JsonResponse(json.dumps({'success': success, 'url': '/home', 'error': error}))

class SignUpElement(Element):
    def _prepare(self):
        self.context = {
            'data_id': self.signup.key
        }
    
    @staticmethod
    @cb.register
    def signup(request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        password2 = request.GET.get('password2')
        success = False
        error = ''
        if email_re.search(username):
            try:
                User.objects.get(username = username)
            except User.DoesNotExist:
                pass
            else:
                error = 'Username Exists'
            if not error:
                if not password == password2:
                    error = 'Passwords do not match'
                elif len(password) < 6:
                    error = 'Minimum length of password is 6'
            if not error:
                user = User.objects.create_user(username = username, email = username, password = password)
                M.UserProfile.objects.create(user=user)
                user.first_name = username.split('@')[0]
                user.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                success = True
        else:
            error = 'Invalid email address'
        return JsonResponse(json.dumps({'success': success, 'url': '/home', 'error': error}))

class RecoElement(Element):
    
    def _prepare(self):
        list_tmplt = '%s+%d+%s'
        lists = M.UserMovieList.objects.filter(user=self.user, movie=self.client.movie)
        rating = M.MovieRating.objects.filter(user=self.client.user_from, movie=self.client.movie)[0].rating
        li = len(lists) and lists[0].list or ''
        is_cl = len(M.UserMovieList.objects.filter(user=self.user, movie=self.client.movie, list='CL'))
        self.context = {
                        'id': self.client.id,
                        'user_from': self.client.user_from,
                        'movie': self.client.movie,
                        'ts': self.client.timestamp,
                        'comment': self.client.comment,
                        'rating': rating,
                        'iswarn': rating<0,
                        'list': li,
                        'is_cl': is_cl,
                        'recommend': '%s+%d' % (recommend.key, self.client.movie.id,),
                        'cl_list': list_tmplt % (add_to_list.key, self.client.movie.id, 'CL'),
                        'wl_list': list_tmplt % (add_to_list.key, self.client.movie.id, 'WL'),
                        'sl_list': list_tmplt % (add_to_list.key, self.client.movie.id, 'SL'),
                        'fl_list': list_tmplt % (add_to_list.key, self.client.movie.id, 'FL'),
                        'followers': self.user.follower.all(),
                        'delete': '%s+%d' % (self.delete.key, self.client.id,),
                        }
    
    @staticmethod
    @cb.register
    def delete(request):
        id = int(request.GET.get('data_id').split('+')[1])
        reco = M.Reco.objects.get(id=id)
        user = request.user.userprofile
        if user == reco.user_from:
            M.Reco.objects.filter(user_from=user, movie=reco.movie).delete()
            return JsonResponse(json.dumps({'success': True}))
        if user == reco.user_to:
            reco.delete()
            return JsonResponse(json.dumps({'success': True}))
        return JsonResponse(json.dumps({'success': False}))
        
class ListElement(Element):
    
    def _prepare(self):
        list_tmplt = '%s+%d+%s'
        is_cl = len(M.UserMovieList.objects.filter(user=self.user, movie=self.client.movie, list='CL'))
        lists = M.UserMovieList.objects.filter(user=self.user, movie=self.client.movie)
        li = len(lists) and lists[0].list or ''
        self.context = {
                        'id': self.client.id,
                        'movie': self.client.movie,
                        'list': li, #self.client.list,
                        'is_cl': is_cl,
                        'recommend': '%s+%d' % (recommend.key, self.client.movie.id,),
                        'cl_list': list_tmplt % (add_to_list.key, self.client.movie.id, 'CL'),
                        'wl_list': list_tmplt % (add_to_list.key, self.client.movie.id, 'WL'),
                        'sl_list': list_tmplt % (add_to_list.key, self.client.movie.id, 'SL'),
                        'fl_list': list_tmplt % (add_to_list.key, self.client.movie.id, 'FL'),
                        'followers': self.user.follower.all(),
                        }

class MovieDetailElement(Element):
    
    def _prepare(self):
        list_tmplt = '%s+%d+%s'
        lists = M.UserMovieList.objects.filter(user=self.user, movie=self.client)
        li = len(lists) and lists[0].list or ''
        is_cl = len(M.UserMovieList.objects.filter(user=self.user, movie=self.client, list='CL'))
        self.context = {'movie': self.client,
                        'list': li,
                        'is_cl': is_cl,
                        'recommend': '%s+%d' % (recommend.key, self.client.id,),
                        'cl_list': list_tmplt % (add_to_list.key, self.client.id, 'CL'),
                        'wl_list': list_tmplt % (add_to_list.key, self.client.id, 'WL'),
                        'sl_list': list_tmplt % (add_to_list.key, self.client.id, 'SL'),
                        'fl_list': list_tmplt % (add_to_list.key, self.client.id, 'FL'),
                        'followers': self.user.follower.all(),
                        }

class RecommenderElement(Element):
    
    def _prepare(self):
        self.context = {'name':self.client.user,
                        'is_following': self.client.user in self.user.follow.all(),
                        'data_id': '%s+%d' % (follow.key, self.client.user.id,),}

class ReviewElement(Element):
    
    def _prepare(self):
        self.context = {'review':self.client.review,
                        'user': self.client.user,
                        'ts': self.client.timestamp}

class UserElement(Element):
    def _prepare(self):
        
        self.context = {'user': self.client,
                        'logged_user': self.user,
                        'is_following': self.client in self.user.follow.all(),
                        'data_id': '%s+%d' % (follow.key, self.client.id,),
                        'follower': self.client.follower.all(),
                        'following': self.client.follow.all(),
                        'other': not self.client == self.user,
                        'edit': self.edit.key,}
    @staticmethod
    @cb.register
    def edit(request):
        get = request.GET
        u = request.user
        up = u.userprofile
        u.first_name = get.get('first_name','')
        u.last_name = get.get('last_name')
        up.title = get.get('title')
        u.save()
        up.save()
        return HttpResponse('ok')

class SearchElement(Element):
    def _prepare(self):
        self.context = {'q': self.client or '', 'data_id': self.query.key}
    
    @staticmethod
    @cb.register
    def query(request):
        q = escape(request.GET.get('query'))
        query_url = 'e_name:(%s) e_alternative_name:(%s) e_original_name:(%s)' % (q,q,q)
        query_url = urllib2.quote(query_url)
        static_url = settings.SOLR_URL + 'q=%s'
        conn = urllib2.urlopen(static_url % query_url + '&version=2.2&wt=python&rows=10&start=0&qt=standard&fl=name%2Cid')
        rsp = ast.literal_eval(conn.read())    
        result = [e for e in rsp['response']['docs']]
        ret = {
            'query':q,
            'suggestions': [e['name'] for e in result],
            'data': [e['id'] for e in result]
        }
        return JsonResponse(json.dumps(ret))
        
class SearchResultElement(Element):
    
    def _prepare(self):
        list_tmplt = '%s+%d+%s'
        lists = M.UserMovieList.objects.filter(user=self.user, movie=self.client)
        li = len(lists) and lists[0].list or ''
        is_cl = len(M.UserMovieList.objects.filter(user=self.user, movie=self.client, list='CL'))
        self.context = {'movie': self.client,
                        'list': li,
                        'is_cl': is_cl,
                        'recommend': '%s+%d' % (recommend.key, self.client.id,),
                        'cl_list': list_tmplt % (add_to_list.key, self.client.id, 'CL'),
                        'wl_list': list_tmplt % (add_to_list.key, self.client.id, 'WL'),
                        'sl_list': list_tmplt % (add_to_list.key, self.client.id, 'SL'),
                        'fl_list': list_tmplt % (add_to_list.key, self.client.id, 'FL'),
                        'followers': self.user.follower.all(),
                        }

class SearchResultUserElement(Element):
    def _prepare(self):
        self.context = {'name':self.client,
                        'is_following': self.client in self.user.follow.all(),
                        'data_id': '%s+%d' % (follow.key, self.client.id,),}

class FeedbackElement(Element):
    def _prepare(self):
        self.context = {'data_id': self.get_fb.key, 'username': self.user.user.first_name, 'userid': self.user.id}
    
    @staticmethod
    @cb.register
    def get_fb(request):
        print request.GET
        return HttpResponse('ok')

class ListListElement(Element):
    def _prepare(self):
        self.context = {'name': self.client.name,
                        'id': self.client.id}