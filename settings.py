# This file should not be edited (as it is apart of the project)
# Any customization of these settings should be within settings_local.py

import os
import sys

MAP_VERSION       = "1.2"

PROJECT_FOLDER    = os.path.dirname(os.path.abspath(__file__))
APP_FOLDER        = os.path.join(PROJECT_FOLDER, 'apps')
INC_FOLDER        = os.path.join(PROJECT_FOLDER, 'third-party')
TEMPL_FOLDER      = os.path.join(PROJECT_FOLDER, 'templates')
ROOT_URLCONF      = os.path.basename(PROJECT_FOLDER) + '.urls'
MEDIA_ROOT        = os.path.join(PROJECT_FOLDER, 'static')

# Add local apps folder to python path
sys.path.append(APP_FOLDER)
sys.path.append(INC_FOLDER)

TIME_ZONE         = 'America/New_York'
LANGUAGE_CODE     = 'en-us'
SITE_ID           = 1
USE_I18N          = False

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"apps.map_context",
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
)

MIDDLEWARE_CLASSES = [
	'api.MapMiddleware',
	'apps.DisableCSRF', # :(
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.cache.UpdateCacheMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.cache.FetchFromCacheMiddleware',
]

TEMPLATE_DIRS = (TEMPL_FOLDER,)

INSTALLED_APPS = (
	'campus',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
)

TINYMCE_DEFAULT_CONFIG = {
	'theme': "advanced",
	'theme_advanced_buttons1' : "%s,|,%s,|,%s,|,%s" % (
			"bold,italic,underline",
			"bullist,numlist,link|,outdent,indent,blockquote",
			"justifyleft,justifycenter,justifyright,justifyfull",
			"formatselect,|,removeformat,code" ),
	'theme_advanced_buttons2' : "",
	'theme_advanced_buttons3' : "",
	'theme_advanced_buttons4' : "",
	'theme_advanced_toolbar_location' : "top",
	'theme_advanced_toolbar_align' : "left",
	'theme_advanced_statusbar_location' : "bottom",
	'theme_advanced_resizing' : True,
}


LOGGING = {
	'version':1,
	'disable_existing_loggers':True,
	'filters': {
		'require_debug_true': {
			'()': 'logs.RequiredDebugTrue',
		},
		'require_debug_false': {
			'()': 'logs.RequiredDebugFalse',
		}
	},
	'formatters': {
		'talkative': {
			'format':'%(levelname)s: %(asctime)s %(module)s %(funcName)s %(message)s'
		},
		'concise': {
			'format':'%(levelname)s: %(message)s (%(asctime)s)'
		}
	},
	'handlers': {
		'discard': {
			'level':'DEBUG',
			'class':'django.utils.log.NullHandler'
		},
		'console': {
			'level':'DEBUG',
			'class':'logging.StreamHandler',
			'formatter':'concise',
			'filters': ['require_debug_true']
		},
		'file': {
			'level': 'INFO',
			'class':'logging.FileHandler',
			'filename':'logs/application.log',
			'formatter':'concise',
			'filters': ['require_debug_false']
		}
	},
	'loggers': {
		'django': {
			'handlers':['discard'],
			'propogate': True,
			'level':'INFO'
		},
		'campus.views': {
			'handlers':['console', 'file'],
			'level':'DEBUG'
		},
		'views': {
			'handlers':['console', 'file'],
			'level':'DEBUG'
		}
	}
}

# For Google to render KML layers, it needs to import the map data.  If working
# locally or behind a firewall, this will not be possible.  If GOOGLE_CAN_SEE_ME
# if false, will fall back to GOOGLE_LOOK_HERE (leave off trailing slash)
GOOGLE_CAN_SEE_ME = True
GOOGLE_LOOK_HERE  = "http://map.ucf.edu"

# TODO: open all data to be indexed by a real search engine, otherwise
# search returns a very basic (nearly useless) keymatch result
SEARCH_ENGINE = None

# Phonebook search service url
PHONEBOOK = "http://webcom.dev.smca.ucf.edu/people/service.php"

# Organization search service URL
ORGANIZATION_SEARCH_URL = 'http://webcom.dev.smca.ucf.edu/search/webroot/service.php'

# Allows for debug to be false in dev
SERVE_STATIC_FILES = False

# Search Query Cache Prefix
SEARCH_QUERY_CACHE_PREFIX = 'search_'

CACHE_TIMEOUT   = 60*60*24
CACHE_LOCATION  = os.path.join(PROJECT_FOLDER, 'cache')
CACHE_BACKEND   = 'file://%s?timeout=%d' % (CACHE_LOCATION, CACHE_TIMEOUT)
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

try:
	from settings_local import *
except ImportError:
	from django.core.exceptions import ImproperlyConfigured
	raise ImproperlyConfigured(
		'Local settings file was not found. ' +
		'Ensure settings_local.py exists in project root.'
	)
