import logging
from logging.handlers import TimedRotatingFileHandler
from twisted.web import http
from twisted.internet import threads
from lsk_scrapers.api import lib


def log(msg, level='debug'):
    print "%s: %s" % (level.upper(), msg)


def get_params(request):
    '''
    retrieve request params and add to dict
    '''
    try:
        params = {}
        for key, val in request.args.items():
            params[key] = val[0]
        log('request params - %s' % params, 'debug')
        return params
    except Exception, err:
        log('get_params() fail - %r' % err, 'error')
        raise err


def write_response(response, request):
    '''
    write http response
    '''
    try:
        request.write(str(response))
        log('sending http response: %s' % response, 'debug')
        request.finish()
    except Exception, err:
        log('write_response() fail - %r' % err, 'error')
        write_error(request, 'error')


def write_error(request, error):
    '''
    write error on http response
    '''
    try:
        request.write('ERROR: %s' % str(error))
        log('sending http response with error: %s' % str(error), 'debug')
        request.finish()
    except Exception, err:
        log('write_error() fail - %r' % err, 'error')
        return


def process_request(request):
    '''
    '''
    try:
        params = get_params(request)
        print params
        assert "name" in params
        assert "channel" in params
        resp = lib.query(params)
        message = lib.construct_message(resp)
        if params['channel'] == "sms":
            write_response(message, request)
        else:
            write_response(resp, request)
    except AssertionError:
        write_error(request, "Missing Parameter")


def get_pages():
    '''
    returns mapping of endpoint : process function
    '''
    return {'/lsk': process_request}


def catch_error(*args):
    for arg in args:
        log('error from deffered - %r' % arg, 'error')
    return 'system error'


class requestHandler(http.Request):

    pages = get_pages()

    def __init__(self, channel, queued):
        http.Request.__init__(self, channel, queued)

    def process(self):
        if self.path in self.pages:
            handler = self.pages[self.path]
            d = threads.deferToThread(handler, self)
            d.addErrback(catch_error)
            return d
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.write('404 - page not found')
            self.finish()


class requestProtocol(http.HTTPChannel):
    requestFactory = requestHandler


class RequestFactory(http.HTTPFactory):
    protocol = requestProtocol
    isLeaf = True

    def __init__(self):
        http.HTTPFactory.__init__(self)
