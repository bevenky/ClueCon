from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin URLs:
    url(r'^admin/', include(admin.site.urls)),

    # ClueCon UI URLs
    url(r'^', include('cluecon_ui.urls')),

)
