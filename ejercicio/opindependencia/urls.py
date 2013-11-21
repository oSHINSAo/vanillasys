from django.conf.urls.defaults import *

urlpatterns = patterns('',
	               (r'^add_attack/$', 'opindependencia.views.add_attack'),
			(r'^$', 'opindependencia.views.index'),
			(r'^add_status/$', 'opindependencia.views.add_status'),
			(r'^add_cliente/$', 'opindependencia.views.add_cliente'),
			(r'^add_accion/$', 'opindependencia.views.add_accion'),
			(r'^add_situacion/$', 'opindependencia.views.add_situacion'),
			(r'^add_tipo/$', 'opindependencia.views.add_tipo'),
			(r'^alcance/$', 'opindependencia.views.alcance'),
			(r'^auto_attack/$', 'opindependencia.views.auto_attack'),
			(r'^auto_clientes/$', 'opindependencia.views.auto_clientes'),
			(r'^auto_accion/$', 'opindependencia.views.auto_accion'),
			(r'^auto_situacion/$', 'opindependencia.views.auto_situacion'),
			(r'^auto_twitter/$', 'opindependencia.views.auto_twitter'),
			(r'^auto_graficas/$', 'opindependencia.views.auto_graficas'),
			(r'^update/$', 'opindependencia.views.update'),



)
