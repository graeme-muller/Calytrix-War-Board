from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    # Home View
    url(r'^days_remaining/$', 'main.jira.greenhopper.ajax.days_remaining', name='days_remaining'),
    url(r'^project_progress/$', 'main.jira.greenhopper.ajax.project_progress', name='project_progress'),
)
