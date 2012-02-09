from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    # Home View
    (r'^(?P<type>\d+)/(?P<level>\d+)/(?P<boxsize>\d+)/(?P<offset>\d+)/qr.png$', 'qrcode.views.qrcode'),
    (r'^$', 'qrcode.views.home'),
)
