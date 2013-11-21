from django.conf.urls.defaults import *

urlpatterns = patterns('',
	               	(r'^nuevo/$', 'bitacora.views.nuevo'),
			(r'^$', 'bitacora.views.index'),
			(r'^index2/$', 'bitacora.views.index2'),
			(r'^index3/$', 'bitacora.views.index3'),
			(r'^logout/$', 'bitacora.views.logout'),
	               	(r'^add/$', 'bitacora.views.add'),
	               	(r'^update/$', 'bitacora.views.update'),
	               	(r'^save/$', 'bitacora.views.save'),
	               	(r'^bitacora/$', 'bitacora.views.bitacora'),
	               	(r'^asignar/$', 'bitacora.views.asignar'),
	               	(r'^activar/$', 'bitacora.views.activar'),
	               	(r'^privilegios/$', 'bitacora.views.privilegios'),
	               	(r'^notify/$', 'bitacora.views.notify'),
	               	(r'^asignados/$', 'bitacora.views.asignados'),
	               	(r'^abiertos/$', 'bitacora.views.abiertos'),
	               	(r'^total/$', 'bitacora.views.total'),
	               	(r'^eliminar/$', 'bitacora.views.eliminar'),
	               	(r'^tomar/$', 'bitacora.views.tomar'),
	               	(r'^reasignar/$', 'bitacora.views.reasignar'),
	               	(r'^perfil/$', 'bitacora.views.perfil'),
	               	(r'^delete_user/$', 'bitacora.views.delete_user'),
	               	(r'^detalles/$', 'bitacora.views.detalles'),
	               	(r'^recuperar/$', 'bitacora.views.recuperar'),
	               	(r'^ventana/$', 'bitacora.views.ventana'),
	               	(r'^window_notification/$', 'bitacora.views.window_notification'),

	               	(r'^eliminar_ventana/$', 'bitacora.views.eliminar_ventana'),
)
