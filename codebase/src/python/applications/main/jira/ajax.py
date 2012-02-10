from django.http import HttpResponse

import contrib.jira_rest_utils as JIRA

import logging
LOGGER = logging.getLogger(__name__)


def get_data(request):
    rest_url = 'greenhopper/1.0/days-remaining/getVersionInfo'
    rest_params = {'projectId': '10030','versionId':'auto' }

    return HttpResponse( JIRA.do_get(rest_url, rest_params) )


def get_greenhopp(request):
    rest_url = 'greenhopper/1.0/days-remaining/getVersionInfo'
    rest_params = {'projectId': '10030','versionId':'auto' }

    return HttpResponse( JIRA.do_get(rest_url, rest_params) )