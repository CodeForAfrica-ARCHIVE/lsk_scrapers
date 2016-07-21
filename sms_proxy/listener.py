import logging, requests
from logging.handlers import TimedRotatingFileHandler
from twisted.web import http
from twisted.internet import threads
from lsk_scrapers.config import API
import smstools


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


def setup(func):
    '''
    decorator that extracts http parameters
    from requests object and adds them to `params` dict

    '''
    def __inner(request):
        try:
            params = get_params(request)
            func(params, request)
        except Exception, err:
            error = 'setup() fail - %r' % err
            log(error, 'error')
            raise err
    return __inner


@setup
def forward_request(params, request):
    '''
    '''
    args = {}
    args['name'] = str(params['Body']).strip()
    args['channel'] = 'sms'
    args['phone_number'] = str(params['From'])
    print "proxy - %s -- %s" % (params, args)
    resp = requests.get('http://localhost:%s/lsk' % API['port'], args)
    smsresp = smstools.send_message(resp.text, args['phone_number'])
    print "sms - %s - %s" % (smsresp, args)

    write_response("%s | %s" % (resp.status_code, resp.text), request)

def get_pages():
    '''
    returns mapping of endpoint : process function
    '''
    return {'/sms/incoming': forward_request}


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
