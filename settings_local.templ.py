# production:
#DEBUG                      = False
#SERVE_STATIC_FILES         = False
#TEMPLATE_DEBUG             = DEBUG

# development
DEBUG                      = True
SERVE_STATIC_FILES         = True
TEMPLATE_DEBUG             = DEBUG
TEMPLATE_STRING_IF_INVALID = 'halp!'


ADMINS         = (
	#('Your Name', 'your_email@domain.com'),
)
MANAGERS       = ADMINS

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# Make this unique, and don't share it with anybody.
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = '**************************************************'

DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.sqlite3',   # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME'     : 'data/map.sqlite3.db',          # Or path to database file if using sqlite3, ex: data/sqlite3.db
        'USER'     : '',                             # Not used with sqlite3.
        'PASSWORD' : '',                             # Not used with sqlite3.
        'HOST'     : '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT'     : '',                             # Set to empty string for default. Not used with sqlite3.
    }
}

# INTERNAL_IPS = ['127.0.0.1',]


# Read settings.py for more details about these settings
#GOOGLE_CAN_SEE_ME = False
#GOOGLE_LOOK_HERE  = "http://map.ucf.edu"