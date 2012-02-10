from django.conf.urls.defaults import patterns, include, url
urlpatterns = patterns('',
    (r'^greenhopper/', include('main.jira.greenhopper.urls', namespace='greenhopper', app_name='main')),
)
