from master import models as M
from django.conf import settings
import base64
import hashlib
import hmac
try:
    import json
except ImportError:
    import simplejson as json
import xmlrpclib
import time
import ast
import urllib2, urllib
import facebook
from django.template.defaultfilters import slugify

SERVER = s = xmlrpclib.Server('http://localhost:7777/', allow_none=True)

FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID', '')
FACEBOOK_API_KEY = getattr(settings, 'FACEBOOK_API_KEY', '')
FACEBOOK_SECRET_KEY = getattr(settings, 'FACEBOOK_SECRET_KEY', '')

MSG_STR = {
    'WL': 'wants to watch',
    'SL': 'has watched',
    'FL': 'does not like'
}

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
            M.Activity.objects.filter(user=user, movie=movie).delete()
            message = '<a href="/user/%(user_id)d/%(user_slug)s">%(user)s</a> %(list)s <a href="/movie/%(movie_id)d/%(movie_slug)s">%(movie)s</a>.' % {'user_id': user.id,
                                            'movie_id' : movie.id, 'user': user.user.first_name, 'list': MSG_STR[li], 'movie': movie, 'movie_slug': slugify(movie.name),
                                            'user_slug': slugify(user.user.first_name)}
            M.Activity.objects.create(user=user, message=message, movie=movie)
            try:
                SERVER.added(m.id)
            except:pass
            return
    m = M.UserMovieList.objects.create(user=user, movie=movie, list=li)
    M.Activity.objects.filter(user=user, movie=movie).delete()
    message = '<a href="/user/%(user_id)d/%(user_slug)s">%(user)s</a> %(list)s <a href="/movie/%(movie_id)d/%(movie_slug)s">%(movie)s</a>.' % {'user_id': user.id,
                                            'movie_id' : movie.id, 'user': user.user.first_name, 'list': MSG_STR[li], 'movie': movie, 'movie_slug': slugify(movie.name),
                                            'user_slug': slugify(user.user.first_name)}
    M.Activity.objects.create(user=user, message=message, movie=movie)
    try:
        SERVER.added(m.id)
    except:pass
    
def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor 
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def parse_signed_request(signed_request):
    secret = settings.FACEBOOK_SECRET_KEY
    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        return data
    
def tweet(movie, rating):
    if rating < 0:
        settings.API.update_status('#Warned - %s #movie #cineight' % str(movie))
    else:
        settings.API.update_status('#Recommended - %s #movie #cineight' % str(movie))
    

def recommend(user, movie, comment="", rating=5):
    followers = user.follower.all()
    
    obj, created = M.Reco.objects.get_or_create(user_from=user, user_to=M.UserProfile.objects.get(id=1), movie = movie, defaults = {'comment':comment})
    obj.comment = comment
    obj.save()
    
    robj, rcreated = M.MovieRating.objects.get_or_create(user=user, movie=movie, defaults={'rating':rating})
    robj.rating = rating
    robj.save()
    
    obj2, created = M.MovieReview.objects.get_or_create(user=user, movie=movie, defaults={'review': comment})
    obj2.review = comment
    obj2.save()
    li = rating > 0 and 'SL' or 'FL'
    if not M.UserMovieList.objects.filter(user=user, movie=movie, list=li).count():
        _add_to_list(user, movie, li)
        
    if created:
        try:
            SERVER.reco_add(user.id, obj.id)
        except:pass
    else: return
    
    for f in followers:
        obj, created = M.Reco.objects.get_or_create(user_from=user, user_to=f, movie = movie, defaults = {'comment':comment})
        obj.comment = comment
        obj.save()
        if created:
            try:
                SERVER.reco_add(f.id, obj.id)
            except:pass
    
    

def exact_search(name):
    name = escape(name)
    query_url = 'name:"%s" alternative_name:"%s" original_name:"%s"' % (name, name, name,)
    query_url = urllib2.quote(query_url.encode('utf-8'))
    static_url = settings.SOLR_URL + 'q=%s&version=2.2&wt=python&rows=1&start=0&qt=standard&fl=id'
    conn = urllib2.urlopen(static_url % query_url)
    rsp = ast.literal_eval(conn.read())    
    result = [e['id'] for e in rsp['response']['docs']]
    if result:return result[0]
    
    query_dict = {'query':name}
    query_url = '_val_:"scale(log(sum(votes,1)),0,10)"^10 name:(%(query)s)^5 name:"%(query)s"^10 alternative_name:(%(query)s)^3 alternative_name:"%(query)s"^3 original_name:(%(query)s)^3 original_name:"%(query)s"^3' % query_dict
    query_url = urllib2.quote(query_url.encode('utf-8'))
    static_url = settings.SOLR_URL + 'q=%s&version=2.2&wt=python&rows=1&start=0&qt=standard&fl=id'
    conn = urllib2.urlopen(static_url % query_url)
    rsp = ast.literal_eval(conn.read())    
    result = [e['id'] for e in rsp['response']['docs']]
    if result:return result[0]
    return None
    
def get_graph(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES,
                                               'undefined',
                                               FACEBOOK_SECRET_KEY)
    if cookie:
            uid = cookie['uid']
            access_token = cookie['access_token']
    else:
        # if cookie does not exist
        # assume logging in normal way
        params = {}
        params["client_id"] = FACEBOOK_APP_ID
        params["client_secret"] = FACEBOOK_SECRET_KEY
        #params["redirect_uri"] = '%s://%s%s' % (
        #             'https' if request.is_secure() else 'http',
        #             Site.objects.get_current().domain,
        #             reverse("socialauth_facebook_login_done"))
        params["redirect_uri"] = "http://apps.facebook.com/cineight/"
        params["code"] = request.GET.get('code', '')

        url = ("https://graph.facebook.com/oauth/access_token?"
               + urllib.urlencode(params))
        from cgi import parse_qs
        userdata = urllib.urlopen(url).read()
        res_parse_qs = parse_qs(userdata)
        # Could be a bot query
        if not res_parse_qs.has_key('access_token'):
            return None
                
        access_token = res_parse_qs['access_token'][-1]
        #graph = facebook.GraphAPI(access_token)
        #uid = graph.get_object('me')['id']
    return facebook.GraphAPI(access_token)
    
def get_fb_movies(request):
    graph = get_graph(request)
    movies = graph.request("me/movies")
    return filter(None, [exact_search(e['name']) for e in movies['data']])

def get_fb_friends(request):
    graph = get_graph(request)
    friends = graph.get_connections("me", "friends")
    return [e['id'] for e in friends['data']]
    return []
    