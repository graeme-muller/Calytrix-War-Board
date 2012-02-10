import os
import sys
import datetime
import logging

import settings

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext, loader
from django.views import debug
from django.template.context import Context

LOGGER = logging.getLogger(__name__)

##
#  This is the login page
#
def do_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                next = '/main/'
                if request.GET:
                    next = request.GET.get('next', next)
                return HttpResponseRedirect(next);
            else:
                # Return a 'disabled account' error message
                return HttpResponse("Disabled account!");
        else:
            # Return an 'invalid login' error message.\
            return HttpResponse("Invalid login");
    else:
        # Show the login page
        template = 'main/login.html'
        t = loader.get_template(template)
        c = RequestContext(request, {
            'form': AuthenticationForm(),
        });
        return HttpResponse(t.render(c))


def do_logout(request):
    logout(request)
    return HttpResponseRedirect('/main/')


def home(request):
    template = 'main/core.html'
    t = loader.get_template(template)
    c = RequestContext(request, {
    });
    return HttpResponse(t.render(c))


def theme_test(request):
    template = 'main/theme_test.html'
    t = loader.get_template(template)
    c = RequestContext(request, {
    });
    return HttpResponse(t.render(c))


@login_required()
def login_required_test(request):
    template = 'main/login_required_test.html'
    t = loader.get_template(template)
    c = RequestContext(request, {
    });
    return HttpResponse(t.render(c))


def server_error_404(request, template_name="404.html"):
    """
    Custom 404 handler method.

    The traceback is written to an html file and a plain text file
    which are placed in the log directory.
    """
    file_prefix = datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')
    ex_type, ex_value, ex_traceback = sys.exc_info() #@UnusedVariable
    try:
        # --- Log to file ---
        # Log straight to file with Django's normal 404 output
        traceback_404 = debug.technical_404_response(request, ex_value)
        destFilename = "%s_%s_404.html" %(file_prefix, settings.LOG_FILE)
        log_filepath = os.path.join(settings.LOG_DIR, destFilename)
        out_file = open(log_filepath, "w")
        out_file.write(traceback_404.content)
        out_file.close()

        # --- Render to page ---
        # Initialise Django's TECHNICAL_404_TEMPLATE to ours
        from main.httpd_errors import FLAT_404_TEMPLATE
        debug.TECHNICAL_404_TEMPLATE = FLAT_404_TEMPLATE
        traceback_404 = debug.technical_404_response(request, ex_value)
        destFilename = "%s_%s_404.log" %(file_prefix, settings.LOG_FILE)
        log_filepath = os.path.join(settings.LOG_DIR, destFilename)
        out_file = open(log_filepath, "w")
        out_file.write(traceback_404.content)
        out_file.close()

        # print request.path

        # --- Render to page ---
        # get our own custom technical 500 template to render for the browser
        # Initialise Django's TECHNICAL_500_TEMPLATE to ours
        from main.httpd_errors import TECHNICAL_404_TEMPLATE
        debug.TECHNICAL_404_TEMPLATE = TECHNICAL_404_TEMPLATE
        traceback_404 = debug.technical_404_response(request, ex_value)
        # now render the actual page
        template = loader.get_template(template_name) # You need to create a 404.html template!
        c = Context({
                     'traceback': traceback_404.content,
                     'log_filepath': log_filepath,
                     })
        response = HttpResponse(template.render(c))
    except Exception, e:
        response = HttpResponse('<html><body><p>%s</p>Click here to return <a href="/">home</a></body></html>' % unicode(e))

    response.status_code = 404
    return response


def server_error_500(request, template_name='500.html'):
    """
    Custom 500 handler method.

    The traceback is written to an html file and a plain text file
    which are placed in the log directory.
    """
    file_prefix = datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')
    try:
        # --- Log to file ---
        # Log straight to file with Django's normal HTML formatted 500 output
        traceback_500 = debug.technical_500_response(request, *sys.exc_info())
        destFilename = "%s_%s_500.html" %(file_prefix, settings.LOG_FILE)
        log_filepath = os.path.join(settings.LOG_DIR, destFilename)
        out_file = open(log_filepath, "w")
        out_file.write(traceback_500.content)
        out_file.close()

        # --- Render to flat file ---
        # get our own custom technical 500 template to render a non-HTML
        # plain text version of the error output
        # Initialise Django's TECHNICAL_500_TEMPLATE to ours
        from main.httpd_errors import FLAT_500_TEMPLATE
        debug.TECHNICAL_500_TEMPLATE = FLAT_500_TEMPLATE
        traceback_500 = debug.technical_500_response(request, *sys.exc_info())
        destFilename = "%s_%s_500.log" %(file_prefix, settings.LOG_FILE)
        log_filepath = os.path.join(settings.LOG_DIR, destFilename)
        out_file = open(log_filepath, "w")
        out_file.write(traceback_500.content)
        out_file.close()

        # --- Render to page ---
        # get our own custom technical 500 template to render for the browser
        # Initialise Django's TECHNICAL_500_TEMPLATE to ours
        from main.httpd_errors import TECHNICAL_500_TEMPLATE
        debug.TECHNICAL_500_TEMPLATE = TECHNICAL_500_TEMPLATE
        # Get the traceback formatted the way we want it for inclusion in the
        # web page we will render
        traceback_500 = debug.technical_500_response(request, *sys.exc_info())
        template = loader.get_template(template_name) # You need to create a 500.html template!
        c = Context({
                     'traceback': traceback_500.content,
                     'log_filepath': log_filepath,
                     })
        response = HttpResponse(template.render(c))
    except Exception, e:
        response = HttpResponse('<html><body><p>%s</p>Click here to return <a href="/">home</a></body></html>' % unicode(e))

    response.status_code = 500
    return response
