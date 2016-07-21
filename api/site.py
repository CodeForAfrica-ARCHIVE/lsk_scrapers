#!/usr/bin/python2.7
from twisted.application import internet, service
from twisted.web import server, resource
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor
from lsk_scrapers.api.api import RequestFactory
from lsk_scrapers.config import API

ProfilerService = internet.TCPServer(API['port'], RequestFactory())
ProfilerService.setName('lsk-ke-api')
application = service.Application('lsk-ke-api')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile(API['logs'], './logs')
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(API['threads'])
