import requests
from django.utils.simplejson.encoder import JSONEncoder

#==============================================================================
# PUBLIC UTILITY METHODS
#==============================================================================
#------------------------------------------------------------------------------
##
# Handle logging in to Mentor - uses the configured host/port and
# username/password combinations to do this
#
def test():
    url = 'http://community.calytrix.com/jira/rest/greenhopper/1.0/days-remaining/getVersionInfo'
    params = {'projectId': '10030','versionId':'auto' }
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic YW5kcmV3bDozaW5zdDNpTiE='}

    r = requests.get(url, params=params, headers=headers)

    print r.text

#==============================================================================
# PUBLIC UTILITY METHODS
#==============================================================================
#------------------------------------------------------------------------------
##
# Handle logging in to Mentor - uses the configured host/port and
# username/password combinations to do this
#
def do_get( rest_url, params={}, headers={} ):
    url = 'http://community.calytrix.com/jira/rest/%s' % rest_url
    headers.update( { 'Content-Type': 'application/json',
                      'Authorization': 'Basic YW5kcmV3bDozaW5zdDNpTiE='} )
    response = requests.get(url, params=params, headers=headers)
    return response.text


def do_post( rest_url, data={}, headers={} ):
    url = 'http://community.calytrix.com/jira/rest/%s' % rest_url
    headers.update( { 'Content-Type': 'application/json',
                      'Authorization': 'Basic YW5kcmV3bDozaW5zdDNpTiE='} )
    response = requests.get(url, data=data, headers=headers)
    return response.text
