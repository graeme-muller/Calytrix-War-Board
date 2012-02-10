from django.http import HttpResponse

import contrib.jira_rest_utils as JIRA

import logging
LOGGER = logging.getLogger(__name__)

##
#  Gets data associated with the GreenHopper Days Remaining widget
#
#  Expects the request's GET dictionary to contain the following parameters:
#     projectId - REQUIRED - the ID of the project (e.g. 10030)
#     versionId - OPTIONAL - the ID of the version (e.g. auto)
#
def days_remaining( request ):
    print 'days_remaining', request.GET
    rest_url = 'greenhopper/1.0/days-remaining/getVersionInfo'

    defaults = { 'versionId':'auto', }

    params = defaults
    params.update( request.GET )

    return HttpResponse( JIRA.do_get(rest_url, params) )



##
#  Gets data associated with the GreenHopper Project Progress widget
#
#  Expects the request's GET dictionary to contain the following parameters:
#
def project_progress( request ):
    print 'project_progress', request.GET
    rest_url = 'greenhopper/1.0/progress-bar-stats/generate'

    defaults = { 'selectedBoardId': 'auto',
                 'contexts': '2.gh.boards.defaultctx',
                 'width': 500, }
    params = defaults
    params.update( request.GET )

    return HttpResponse( JIRA.do_get(rest_url, params) )
