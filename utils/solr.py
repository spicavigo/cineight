#!/usr/bin/env python
#
#       solr.py
#       
#       Copyright 2010 yousuf <yousuf@postocode53.com>
#       

from django.conf import settings
from urllib2 import urlopen
from urllib import urlencode
import ast

class SOLR(object):
    GET_PARAMS={
    'version':2.2, 'q':'*:*', 'fq':'', 
    'qt':'standard', 'wt':'python', 'hl.simple.pre':'<b>', 'hl.simple.post':'</b>'
        }
    MAX_HL_LENGTH = 200
    
    def __init__(self, fl="*,score", hl="true", hl_fl="", hl_fragsize=70, hl_snippets=5, hl_mergeContiguous="true",
                hl_fragmenter="regex", hl_usePhraseHighlighter="true", hl_regex_slop=0.2, hl_highlightMultiTerm="true",
                start=0, rows=100, sort = None):
        self.get_params = self.GET_PARAMS.copy()
        self.get_params = self.GET_PARAMS.copy()
        self.get_params['fl'] = fl
        self.get_params['hl'] = hl
        self.get_params['hl.fl'] = hl_fl
        self.get_params['hl.fragsize'] = hl_fragsize
        self.get_params['hl.snippets'] = hl_snippets
        self.get_params['hl.mergeContiguous'] = hl_mergeContiguous
        self.get_params['hl.fragmenter'] = hl_fragmenter
        self.get_params['hl.usePhraseHighlighter'] = hl_usePhraseHighlighter
        self.get_params['hl.regex.slop'] = hl_regex_slop
        self.get_params['hl.highlightMultiTerm'] = hl_highlightMultiTerm
        self.get_params['start'] = start
        self.get_params['rows'] = rows
        if sort:
            self.get_params['sort'] = sort

        
    def search(self, query='', **kwargs):
        if not query:
            return 0,[]           
        url = settings.SOLR_JOB_SEARCH_URL
        for k,v in kwargs.items():
            query += ' ' + k + ':'+ v        
        self.get_params['q'] = query        
        data = urlencode(self.get_params)
        #print url+'?'+data
        u = urlopen(url+'?' + data)
        return self.parse_result(u.read())

    def parse_result(self, data):
        data = ast.literal_eval(data)
        docs = data['response']['docs']
        if self.get_params['hl'] == 'false':
            return data['response']['numFound'], docs
        hls = data['highlighting']
        for e in docs:
            e['hl'] = '...'.join(hls[str(e['id'])].get(self.get_params['hl.fl'], ''))
        return data['response']['numFound'], docs
        

