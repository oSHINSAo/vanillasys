from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User




class Status(models.Model):
	idsta  =  models.AutoField(primary_key = True)
	status  = models.CharField(max_length = 100)
	def __unicode__(self):
		return self.status

class Tipo(models.Model):
	idtip  =  models.AutoField(primary_key = True)
	tipo  = models.CharField(max_length = 100)
	def __unicode__(self):
		return self.tipo

class Clientes(models.Model):
	idcli  =  models.AutoField(primary_key = True)
	cliente  = models.CharField(max_length = 100)
	tipo = models.CharField(max_length = 30)
	peligro = models.BooleanField(default=False)
	def __unicode__(self):
		return self.cliente


class ClientesAttack(models.Model):
	idcla  =  models.AutoField(primary_key = True)
	idcli = models.ForeignKey(Clientes)
	idtip = models.ForeignKey(Tipo)
	consecuencia = models.CharField(max_length = 250)
	idsta = models.ForeignKey(Status)
	fecha = models.DateField(_('Fecha creado'),
					auto_now_add=True, blank=True)
	hora = models.TimeField(_('Hora creado'),
					auto_now_add=True, blank=True)
	fecha_fin = models.DateField(_('Fecha creado'),
					null=True,blank=True)
	hora_fin = models.TimeField(_('Hora creado'),
					null=True,blank=True)
	def __unicode__(self):
		return unicode(self.idcla)

class Situacion(models.Model):
	idacc  =  models.AutoField(primary_key = True)
	situacion = models.CharField(max_length = 400)
	idcla = models.ForeignKey(ClientesAttack)
	fecha = models.DateField(_('Fecha creado'),
					auto_now_add=True, blank=True)
	hora = models.TimeField(_('Hora creado'),
					auto_now_add=True, blank=True)
	fecha_fin = models.DateField(_('Fecha creado'),
					null=True,blank=True)
	hora_fin = models.TimeField(_('Hora creado'),
					null=True,blank=True)
	def __unicode__(self):
		return unicode(self.situacion)


class Acciones(models.Model):
	idacc  =  models.AutoField(primary_key = True)
	accion = models.CharField(max_length = 400)
	idcla = models.ForeignKey(ClientesAttack)
	fecha = models.DateField(_('Fecha creado'),
					auto_now_add=True, blank=True)
	hora = models.TimeField(_('Hora creado'),
					auto_now_add=True, blank=True)
	fecha_fin = models.DateField(_('Fecha creado'),
					null=True,blank=True)
	hora_fin = models.TimeField(_('Hora creado'),
					null=True,blank=True)
	def __unicode__(self):
		return self.accion

class Graficas(models.Model):
	idgra  =  models.AutoField(primary_key = True)
        grafica = models.ImageField(_('Grafica'),upload_to='uploads/opindependencia/')
	idcla = models.ForeignKey(ClientesAttack)

