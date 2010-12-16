#!/usr/bin/env python
#
#       server.py
#       
#       Copyright 2010 yousuf <yousuf@postocode53.com>
#       


from django.core.management import call_command
from django.core.management import setup_environ
from datetime import datetime

import settings
setup_environ(settings)

import json
import master
from master import models as M
from master.element import ListElement, RecoElement

from twisted.application import service, internet
from twisted.application.service import Application
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile

from twisted.internet.protocol import Protocol, Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.web import xmlrpc, server

class CEProtocol(LineReceiver):
    def lineReceived(self, line):
        if self.state == 1:
            self.user = M.UserProfile.objects.get(id=int(line.strip()))
            self.factory.conns[self.user.id] = self
            self.state = 2

    def connectionMade(self):
        self.state = 1

    def connectionLost(self, reason):
        del self.factory.conns[self.user.id]

class CEFactory(Factory):
    protocol = CEProtocol

    def __init__(self):
        self.conns = {}
    
    def send_data(self, user, data):
        self.conns[user].transport.write(json.dumps(data))
  
class CERPC(xmlrpc.XMLRPC):
    def __init__(self, factory):
        self.factory = factory
        xmlrpc.XMLRPC.__init__(self, allowNone=True)
        
    def xmlrpc_added(self, uml):
        try:
            uml = M.UserMovieList.objects.get(id=uml)
            self.factory.send_data(uml.user.id,
                               {'action': 'ADD',
                                'html': ListElement(uml.user, uml).show(),
                                'tab':uml.list,
                                'id': uml.id,
                                'mid': uml.movie.id})
        except Exception, e:
            print e
        return 1
    
    def xmlrpc_removed(self, uml):
        try:
            uml = M.UserMovieList.objects.get(id=uml)
            self.factory.send_data(uml.user.id,
                               {'action': 'DEL',
                                'tab':uml.list,
                                'id': uml.id,
                                'mid': uml.movie.id})
        except Exception, e:
            print e
    
    def xmlrpc_reco_add(self, user, reco):
        try:
            user = M.UserProfile.objects.get(id=int(user))
            reco = M.Reco.objects.get(id=int(reco))
            tab = 'RR'
            if user == reco.user_from:
                tab = 'FR'
            self.factory.send_data(user.id, {
                'action':'ADD',
                'tab': tab,
                'html': RecoElement(user, reco).show(),
            })
        except Exception, e:
            print e
        

factory = CEFactory()
#reactor.listenTCP(7777, server.Site(CERPC(factory)))
#reactor.listenTCP(7778, factory)
#reactor.run()
application = Application("ce_real_time")
logfile = DailyLogFile("cs_real_time.log", "/tmp")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
ceService = service.MultiService()
internet.TCPServer(7777, server.Site(CERPC(factory))).setServiceParent(ceService)
internet.TCPServer(7778, factory).setServiceParent(ceService)
ceService.setServiceParent(application)

