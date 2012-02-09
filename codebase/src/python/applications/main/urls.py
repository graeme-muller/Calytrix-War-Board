from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    # Home View
    (r'^login/$', 'main.views.do_login'),
    (r'^login_required_test/$', 'main.views.login_required_test'),
    (r'^logout/$', 'main.views.do_logout'),
    (r'^theme_test/$', 'main.views.theme_test'),
    (r'^$', 'main.views.home'),
)
