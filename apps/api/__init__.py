import re
from django.conf import settings
from django.core.urlresolvers import reverse, resolve, Resolver404
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseServerError
from django.core.cache import cache
from django.utils.cache import get_cache_key

formats = {
	'json' : {
		'mimetype' : 'application/json',
		'content'  : '{"error":"%s"}',
		},
	'txt'  : {
		'mimetype' : 'text/plain; charset=utf-8',
		'content'  : '%s',
		},
	'kml'  : {
		'mimetype' : 'application/vnd.google-earth.kml+xml',
		'content'  : '<?xml version="1.0"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>%s</name></Document></kml>',
		},
	'xml'  : {
		'mimetype' : 'text/xml',
		'content'  : '<?xml version="1.0"?><error>%s</error>',
		},
	'bxml' : {
		'mimetype' : 'application/xml',
		'content'  : '<?xml version="1.0"?><error>%s</error>',
		},
	'ajax' : {
		'mimetype' : 'text/html; charset=utf-8',
		'content'  : '%s',
		},
}


class HttpResponseNotImplemented(HttpResponse):
	status_code = 501


def MonkeyPatchHttpRequest():
	'''
	Define is_<format> methods on the request object (called in base __init__.py)
	'''
	for format, o in formats.items():
		code = """def is_%s(self): 
					import re 
					return False if re.search('\.%s$', self.path) is None else True""" % (format, format)
		scope = {}
		exec code in scope
		setattr(HttpRequest, 'is_%s' % format, scope['is_%s' % format])


class MapMiddleware(object):
	
	def process_request(self, request):
		'''
		Caching
		django ignores cache if query string is present.
		GET vars not needed for api requests so just removing it to enable cache
		'''
		if request.GET.get('q', False):
			return
		
		for format,spec in formats.items():
			is_api_call = getattr(request, 'is_%s' % format)
			if is_api_call():
				request.GET = {}
				if settings.DEBUG:
					cache_key = get_cache_key(request)
					print "API Cache Key: %s" % cache_key
		
	def process_response(self, request, response):
		'''
		Make sure reponses have right mime type and return Not Implemented server error when appropriate
		'''
		for format,spec in formats.items():
			is_api_call = getattr(request, 'is_%s' % format)
			if is_api_call():
				# view returned bad content type, assuming not implemented
				if response['Content-type'] != spec['mimetype']:
					if response.status_code == 200:
						rsp = dict(spec)
						rsp['content'] = spec['content'] % 'Not Implemented'
						return HttpResponseNotImplemented(**rsp)
					elif response.status_code == 404:
						rsp = dict(spec)
						rsp['content'] = spec['content'] % 'Not Found'
						return HttpResponseNotFound(**rsp)
					elif response.status_code == 500:
						rsp = dict(spec)
						rsp['content'] = spec['content'] % 'Server Error. Bummer'
						return HttpResponseServerError(**rsp)
					else:
						msg = spec['content'] % ('Error %s' % response.status_code)
						response['Content-Type'] = spec['mimetype']
						response._container = [msg]
					
		return response


def handle_request(request, url):
	'''
	API view for detecting format without dirtying the urls file
	'''
	try:
		view, args, kwargs = resolve('/' + url)
	except Resolver404:
		view, args, kwargs = resolve('/' + url + '/')
	kwargs['request'] = request
	return view(*args, **kwargs)