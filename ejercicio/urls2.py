from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'axtel.views.home', name='home'),
    # url(r'^axtel/', include('axtel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^graficas/', include('graficas.urls')),
    (r'^control/', include('control.urls')),

    #(r'^datos/', include('datos.urls')),
    (r'^headline/', include('headline.urls')),

    #(r'^abrir/', 'graficas.views.abrir'),
    #(r'^leer/', 'graficas.views.leer'),
    (r'^incidentes/', include('axtel.incidentes.urls')), 
    (r'^indicadores/', include('axtel.indicadores.urls')), 
    (r'^accounts/', include('registration.urls')),
    (r'^cliente2/$', 'axtel.control.views.cliente2'),
    (r'^$', 'axtel.control.views.index'),

)
