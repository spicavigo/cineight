import urllib2, urllib
from BeautifulSoup import BeautifulSoup
from lxml import html
import re
import sys
import socket
socket.setdefaulttimeout(60)

def get_year(year):
	p=re.compile('^\/title\/tt\d+\/$')
	links = []
	url = 'http://www.imdb.com/search/title?'
	data = {'sort': 'release_date_us,desc', 'start':'1', 'title_type':'feature', 'year':'%d,%d' % (year, year)}
	url = url + urllib.urlencode(data)
	while 1:
		 try:
		     print url
		     u=urllib2.urlopen(url)
		 except:
				 print "Error"
				 break
		 data = u.read()

		 bs=BeautifulSoup(html.tostring(html.fromstring(data), encoding='ascii'))
		 found=False
		 titles = bs.findAll('td', attrs={'class':'title'})

		 res={}
		 for t in titles:
		     res={}

		     r = t.find('div', attrs={'class':'user_rating'})
		     if r:
		         res['rating'] = getattr(r.find('b'), 'string','')

		     res['year'] = getattr(t.find('span',
	attrs={'class':'year_type'}),'string','')
		     res['plot'] = getattr(t.find('span',
	attrs={'class':'outline'}),'string','')
		     res['link'] = getattr(t.find('a', href=p),'string','')
		     res['name'] = t.find('a', href=p).get('href')
		     res['genre']=[]
		     gen = t.find('span', attrs={'class':'genre'})
		     if gen:
		         for g in gen.findAll('a'):
		             res['genre'].append(g.string)
		     print res
		 sys.stdout.flush()
		 
		 for e in bs.find('span', attrs={'class':'pagination'}).findAll('a'):
		     if 'Next' in e.string:
		         links.append(e.get('href'))
		         url='http://www.imdb.com'+e.get('href')
		         found=True
		 if not found:
		     break

for i in range(1900	, 2011):
	print i
	get_year(i)
