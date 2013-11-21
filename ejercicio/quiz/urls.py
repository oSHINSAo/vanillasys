from django.conf.urls.defaults import *

urlpatterns = patterns('',
	               	(r'^add/$', 'quiz.views.add'),
			(r'^$', 'quiz.views.index'),
			(r'^add_pregunta/$', 'quiz.views.add_pregunta'),
			(r'^add_respuesta/$', 'quiz.views.add_respuesta'),
			(r'^add_clave/$', 'quiz.views.add_clave'),
			(r'^contestar/$', 'quiz.views.contestar'),
			(r'^respuestas/$', 'quiz.views.respuestas'),
			(r'^resultados/$', 'quiz.views.resultados'),
			(r'^excel_resultados/$', 'quiz.views.excel_resultados'),
			(r'^del_quiz/$', 'quiz.views.del_quiz'),
			(r'^del_pregunta/$', 'quiz.views.del_pregunta'),
			(r'^del_respuesta/$', 'quiz.views.del_respuesta'),
			(r'^detalles/$', 'quiz.views.detalles'),
			(r'^fin/$', 'quiz.views.fin'),
			(r'^ip/$', 'quiz.views.ip'),
)
