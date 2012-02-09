import os, sys

apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project).replace('/', os.path.sep)
# sys.path.append(workspace)

##
# Add the path to the application and Django.
sys.path.append(os.path.join(workspace,'applications'))
sys.path.append(os.path.join(workspace,'external','django','1.3'))

##
# Set up the environmental variables referred to by the application and Django.
os.environ['TZ'] = 'GMT'
os.environ['APPLICATION_DB'] = r'application_db'
os.environ['APPLICATION_ROOT'] = os.path.split(workspace)[0]
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

##
# Print the path details to Apache's "errors.log" file so we can see what
# it ended up being for debugging purposes
print >> sys.stderr, '='*100
print >> sys.stderr, 'DJANGO: DJANGO_SETTINGS_MODULE is:', os.environ['DJANGO_SETTINGS_MODULE']
print >> sys.stderr, 'DJANGO: APPLICATION_DB is        :', os.environ['APPLICATION_DB']
print >> sys.stderr, 'DJANGO: APPLICATION_ROOT is      :', os.environ['APPLICATION_ROOT']
print >> sys.stderr, 'DJANGO: Python system path is:'
for p in sys.path:
	print >> sys.stderr, '-', p
print >> sys.stderr, '='*100

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()