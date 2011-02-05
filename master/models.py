from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save

# Create your models here.

class Movie(models.Model):
    imdb_rating = models.FloatField()
    votes = models.IntegerField()
    name = models.CharField(max_length = 255)
    url = models.URLField(max_length=255)
    plot = models.TextField()
    popularity = models.FloatField()
    original_name = models.CharField(max_length =255)
    last_modified_at = models.DateTimeField()
    imdb_id = models.CharField(max_length=80)
    released = models.DateField(blank=True, null=True)
    adult = models.BooleanField()
    mtype = models.CharField(max_length=50)
    alternative_name = models.CharField(max_length = 255)
    image = models.CharField(max_length=300, blank=True, null=True)
        
    def __unicode__(self):
        return u'%s(%s)' %(self.name, self.released and self.released.year)

    def _get_link(self):
        return "/movie/%d" % self.id

    link = property(_get_link)
        
class MovieRating(models.Model):
    movie = models.ForeignKey(Movie)
    user = models.ForeignKey('UserProfile')
    rating = models.IntegerField()

    class Meta:
        unique_together = ('movie','user')
        
class MovieReview(models.Model):
    movie = models.ForeignKey(Movie)
    user = models.ForeignKey('UserProfile')
    review = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Reco(models.Model):
    user_from = models.ForeignKey('UserProfile', related_name='r_user_from')
    user_to = models.ForeignKey('UserProfile', related_name='r_user_to')
    movie = models.ForeignKey(Movie)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=255, blank = True)
    is_warn = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s(%d)' %(str(self.movie), self.movie.id)
    
class MovieTag(models.Model):
    movie = models.ForeignKey(Movie)
    tag = models.ForeignKey('Tag')
    user = models.ForeignKey('UserProfile', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserMovieList(models.Model):
    MOVIE_LIST_CHOICES = (('WL', 'Watch List'),
                            ('SL', 'Watched List'),
                            ('FL', 'Filter List'),
                            ('CL', 'Compare List'),
                        )
    user = models.ForeignKey('UserProfile')
    movie = models.ForeignKey('Movie')
    list = models.CharField(max_length=2, choices=MOVIE_LIST_CHOICES)
    timestamp = models.DateTimeField(auto_now=True)
    
class AltName(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie)

class Tag(models.Model):
    name = models.CharField(max_length = 30, db_index=True)

    def __unicode__(self):
        return self.name

class AskReco(models.Model):
    ASK_RECO_CHOICES = (('Y', 'Yes'),
                        ('N', 'No'),
                        )
    user_from = models.ForeignKey('UserProfile', related_name='a_user_from')
    user_to = models.ForeignKey('UserProfile', related_name='a_user_to')
    movie = models.ForeignKey(Movie)
    timestamp = models.DateTimeField(auto_now_add=True)
    answer = models.CharField(max_length=2, choices=ASK_RECO_CHOICES)

class Activity(models.Model):
    user = models.ForeignKey('UserProfile')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey('Movie', blank=True, null=True)
    follow = models.ForeignKey('UserProfile', related_name='follow_activity', blank=True, null=True)

class Message(models.Model):
    user = models.ForeignKey('UserProfile')
    timestamp = models.DateTimeField(auto_now_add=True)
    list = models.ForeignKey('UserMovieList', blank=True, null=True)
    movie = models.ForeignKey('Movie', blank=True, null=True)
    user_from = models.ForeignKey('UserProfile', related_name='user_from', blank=True, null=True)
    msg = models.TextField()
    
class List(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __unicode__(self):
        return u'%s' %(self.name,)
    
class PublicList(models.Model):
    list = models.ForeignKey('List')
    movie  = models.ForeignKey('Movie')
    pos = models.IntegerField()
    
TITLE_CHOICES = (
    ('MG', 'Moviegoer'),
    ('AT', 'Actor'),
    ('DI', 'Director'),
    ('CI', 'Critic'),
)

class FBData(models.Model):
    user = models.ForeignKey('UserProfile')
    movies = models.TextField()
    friends = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follower = models.ManyToManyField('self', related_name='follower_user', symmetrical=False, blank = True, null = True)
    follow = models.ManyToManyField('self', related_name='follow_user', symmetrical=False,  blank = True, null = True)
    title = models.CharField(max_length=2, blank=True, null=True, choices=TITLE_CHOICES)
    def __unicode__(self):
        return self.user.first_name
    
    def _get_link(self):
        return "/user/%d" % self.id

    link = property(_get_link)

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User) 
