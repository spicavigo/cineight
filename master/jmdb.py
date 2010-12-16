from django.db import models

class Akatitle(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    language = models.CharField(max_length=9)
    title = models.CharField(max_length=1200)
    addition = models.CharField(max_length=3000, blank=True)
    class Meta:
        db_table = u'akatitles'


class Certificate(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    country = models.CharField(max_length=150, blank=True)
    certification = models.CharField(max_length=765)
    addition = models.CharField(max_length=3000, blank=True)
    class Meta:
        db_table = u'certificates'

class Colorinfo(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    color = models.CharField(max_length=300)
    addition = models.CharField(max_length=3000, blank=True)
    class Meta:
        db_table = u'colorinfo'

class Country(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    country = models.CharField(max_length=150)
    class Meta:
        db_table = u'countries'

class Crazycredit(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    credittext = models.TextField(blank=True)
    class Meta:
        db_table = u'crazycredits'

class Genre(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    genre = models.CharField(max_length=150)
    class Meta:
        db_table = u'genres'

class Goof(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    gooftext = models.TextField(blank=True)
    class Meta:
        db_table = u'goofs'

class Keyword(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    keyword = models.CharField(max_length=375)
    class Meta:
        db_table = u'keywords'

class Language(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    language = models.CharField(max_length=300)
    class Meta:
        db_table = u'language'

class Movie(models.Model):
    id = models.IntegerField(primary_key=True, db_column='movieid')
    name = models.CharField(max_length=1200, db_column='title')
    year = models.CharField(max_length=300, blank=True)
    imdbid = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'movies'
    
    def __unicode__(self):
        return u'%s(%s)' %(self.name, self.year)

    def _get_rating(self):
        rating = self.rating_set.all()
        if rating:
            return rating[0].rank
        return ''
    
    imdb_rating = property(_get_rating)
    
    def _get_plot(self):
        plot = self.plot_set.all()
        if plot:
            return plot[0].plottext.split('\n')[0]
        return ''
    
    plot = property(_get_plot)
    def _get_link(self):
        return "/movie/%d" % self.id

    link = property(_get_link)

class Plot(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    plottext = models.TextField(blank=True)
    class Meta:
        db_table = u'plots'

class Quote(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    quotetext = models.TextField(blank=True)
    class Meta:
        db_table = u'quotes'

class Rating(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    rank = models.CharField(max_length=12)
    votes = models.IntegerField(null=True, blank=True)
    distribution = models.CharField(max_length=30)
    class Meta:
        db_table = u'ratings'

class Releasedate(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    country = models.CharField(max_length=150, blank=True)
    imdbdate = models.CharField(max_length=150)
    releasedate = models.DateField(null=True, blank=True)
    addition = models.CharField(max_length=3000, blank=True)
    class Meta:
        db_table = u'releasedates'

class Runningtime(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    time = models.CharField(max_length=150)
    addition = models.CharField(max_length=3000)
    class Meta:
        db_table = u'runningtimes'

class Tagline(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    taglinetext = models.TextField(blank=True)
    class Meta:
        db_table = u'taglines'

class Trivia(models.Model):
    movieid = models.ForeignKey('Movie', db_column='movieid')
    triviatext = models.TextField(blank=True)
    class Meta:
        db_table = u'trivia'