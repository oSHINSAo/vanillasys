from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
	idusu  =  models.AutoField(primary_key = True)
	nombre = models.CharField(max_length = 200)
	noemp = models.IntegerField()
    	fecha = models.DateField(_('Fecha creado'),
					auto_now_add=True, blank=True)
    	hora = models.TimeField(_('Hora creado'),
					auto_now_add=True, blank=True)
	def __unicode__(self):
		return self.nombre

class Quiz(models.Model):
	idqui  =  models.AutoField(primary_key = True)
	quiz = models.CharField(max_length = 200)
	codigo = models.CharField(max_length = 100)
    	fecha = models.DateTimeField(_('Fecha creado'),
					auto_now_add=True, blank=True)
	def __unicode__(self):
		return self.quiz

class Pregunta(models.Model):
	idpre  =  models.AutoField(primary_key = True)
    	idqui = models.ForeignKey(Quiz)
	pregunta = models.CharField(max_length = 400)
	def __unicode__(self):
		return self.pregunta

class Respuesta(models.Model):
	idres  =  models.AutoField(primary_key = True)
    	idpre = models.ForeignKey(Pregunta)
	respuesta = models.CharField(max_length = 400)
	def __unicode__(self):
		return self.respuesta

class Clave(models.Model):
	idcla = models.AutoField(primary_key= True)
    	idqui = models.ForeignKey(Quiz)
	clave = models.CharField(max_length= 250)
	def __unicode__(self):
		return self.clave

class Resultado(models.Model):
	idcla = models.AutoField(primary_key= True)
	nombre = models.CharField(max_length = 150)
	noemp = models.IntegerField()
    	fecha = models.DateField(_('Fecha creado'),
					auto_now_add=True, blank=True)
    	hora = models.TimeField(_('Hora creado'),
					auto_now_add=True, blank=True)
    	idqui = models.ForeignKey(Quiz)
	clave = models.CharField(max_length= 250)
	aciertos = models.IntegerField()
	errores = models.IntegerField()	
	calif =  models.DecimalField(max_digits=5, decimal_places=2)
	def __unicode__(self):
		return self.nombre


