from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

if settings.USE_I18N:
    i18n_view = 'django.views.i18n.javascript_catalog'
else:
    i18n_view = 'django.views.i18n.null_javascript_catalog'

urlpatterns = patterns('')

# Serve media as static pages during debug. In production, serve them using Apache.
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    )

urlpatterns += patterns('',
    # Javascript i18n definitions
    (r'^jsi18n/$', i18n_view, {'packages': 'django.conf'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # QR Codes:
    (r'^qrcode/', include('qrcode.urls')),

    # Main:
    (r'^', include('main.urls')),
)

handler404 = 'main.views.server_error_404'
handler500 = 'main.views.server_error_500'