from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Home View
    url (r'^login/$', 'main.views.do_login', name='login'),
        (r'^theme_test/$', 'main.views.theme_test'),
        (r'^(?P<poll_id>\d+)/vote/$', 'main.views.vote'),
        (r'^$', 'main.views.home'),
    
    # User preferences
        (r'^jira/', include('main.jira.urls', namespace='jira', app_name='main')),

    url(r'^$', 'main.views.home', name='home'),
)
