from django.core.management import call_command
from django.core.management import setup_environ
from datetime import datetime
import sys, traceback

import settings
setup_environ(settings)

from master.models import Movie
from movies import MovieDb

m = MovieDb()
total = m.max()
#page = 743, count=22260, total=44008
#count = 22260
#page = 743
count = 0
lcount = 0
page = 1
while count < total:
    x = m.browse(page=page)
    page += 1
    count += len(x)
    if count == lcount:
        break
    lcount = count
    for e in x:
        try:
            imdb_rating=float(e['rating'] or 0)
            votes = int(e['votes'] or 0)
            name=e['name']
            url = e['url']
            plot=e['overview'] or ''
            popularity=float(e['popularity'] or 0)
            original_name = e['original_name'] or ''
            imdb_id = e['imdb_id'] or ''
            adult = e['adult'] == 'true'
            mtype = e['type'] or 'movie'
            id = int(e['id'])
            alternative_name = e['alternative_name'] or ''
            last_modified_at = datetime.strptime(e['last_modified_at'], '%Y-%m-%d %H:%M:%S')
            released = e['released'] and datetime.strptime(e['released'], '%Y-%m-%d').date() or last_modified_at.date()
            try:
                movie = Movie.objects.get(id=int(e['id']))
                if movie.last_modified_at < last_modified_at:
                    movie.imdb_rating = imdb_rating
                    movie.votes = votes
                    movie.name = name
                    movie.url = url
                    movie.plot = plot
                    movie.popularity = popularity
                    movie.original_name = original_name
                    movie.imdb_id = imdb_id
                    movie.adult = adult
                    movie.mtype = mtype
                    movie.alternative_name = alternative_name
                    movie.last_modified_at = last_modified_at
                    movie.released = released
                continue
            except:pass
            try:
                Movie.objects.create(imdb_rating=imdb_rating, votes = votes,
                                     name=name, url = url, plot=plot, popularity=popularity,
                                     original_name = original_name, last_modified_at=last_modified_at, imdb_id = imdb_id,
                                     released = released, adult = adult, mtype = mtype, id = id,
                                     alternative_name = alternative_name)
            except:pass
        except:
            traceback.print_exc(file=sys.stdout)
            print e.items()
    print 'page = %d, count=%d, total=%d' % (page, count, total)
