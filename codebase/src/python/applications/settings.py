# Django settings for zyzygySite project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOG_DIR = r'C:\dev\apache\httpd\2.2.19\logs'
LOG_FILE = r'application' #will be appended with ".log'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ.get('APPLICATION_DB', 'django_app_db'), # Or path to database file if using sqlite3.
        'USER': 'postgres',                                        # Not used with sqlite3.
        'PASSWORD': 'postgres',                                    # Not used with sqlite3.
        'HOST': '',                                                # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                                # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Australia/Perth'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# Non-Django setting. Determines which theme will be used if none is
# explicitly set for a user. Themes are defined in media/css/themes.
# Also @see accounts.models. AVAILABLE_THEMES
DEFAULT_THEME='ui-lightness'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.environ.get('APPLICATION_ROOT'), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'

# URL for login/logout pages. Make sure to use a trailing slash.
# Examples: "/accounts/login/".
LOGIN_URL = '/main/login/'
#LOGOUT_URL = '/main/logout/'
#LOGIN_REDIRECT_URL = '/accounts/profile/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rsfva0u6y8bhe@t}nf0p%9jlwyxc0@ic(y)%6j_#4jabo7g-gl'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
# Be sure to extend the list of existing Django template context
# processors, not overwrite it.
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    'main.context_processors.user_site_profile',
)

# Enabled middleware - be careful of the ordering; the first (top) item will
# be executed last
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware', # best to leave this first in the list!
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# set the class for adding 'extra' fields for get_profile(). Refer to:
# http://docs.djangoproject.com/en/1.3/topics/auth/#storing-additional-information-about-users
# ...for more information
AUTH_PROFILE_MODULE = 'accounts.usersiteprofile'

ROOT_URLCONF = 'urls'

APP_NAMES = (
    'accounts',
    'main',
)

TEMPLATE_DIRS = (
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        os.path.join(os.environ.get('APPLICATION_ROOT'), 'templates').replace('\\','/'),
    )

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.webdesign',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
]
INSTALLED_APPS.extend(APP_NAMES)

LOGGING = {
    'version': 1, 'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s %(asctime)s] %(module)s.%(funcName)s #%(lineno)d: %(message)s'
        },
    },
    'filters': {},
    'handlers':{
        'null':{
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'filename': os.path.join(LOG_DIR, '%s.log' % LOG_FILE),
            'maxBytes': 1024 * 100,
            'backupCount': 10,
        },
    },
    'loggers':{
        'django':{
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request':{
            'handlers': ['console','file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'main.views':{
            'handlers': ['console','file'],
            'level': 'INFO',
            'filters': []
        }
    }
}