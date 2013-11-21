from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
#from filebrowser.sites import site
admin.autodiscover()



urlpatterns = patterns('',
   #url(r'^admin/filebrowser/', include(site.urls)),
    # Examples:
    # url(r'^$', 'axtel.views.home', name='home'),
    # url(r'^axtel/', include('axtel.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^graficas/', include('graficas.urls')),
    (r'^bitacora/', include('bitacora.urls')), 
    (r'^quiz/', include('quiz.urls')), 
    (r'^opindependencia/', include('ejercicio.opindependencia.urls')), 
)
