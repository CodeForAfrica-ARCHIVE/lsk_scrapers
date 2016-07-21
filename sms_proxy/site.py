#!/usr/bin/python2.7
from twisted.application import internet, service
from twisted.web import server, resource
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor

from lsk_scrapers.sms_proxy.listener import RequestFactory
from lsk_scrapers.config import SMS

ProfilerService = internet.TCPServer(SMS['port'], RequestFactory())
ProfilerService.setName('sms-listener')
application = service.Application('sms-listener')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile(SMS['logs'], './logs')
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(SMS['threads'])
