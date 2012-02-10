from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Home View
    url(r'^login/$', 'main.views.do_login', name='login'),
    url(r'^logout/$', 'main.views.do_logout', name='logout'),

    # User preferences
    (r'^jira/', include('main.jira.urls', namespace='jira', app_name='main')),

    url(r'^$', 'main.views.home', name='home'),
)
