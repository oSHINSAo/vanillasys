from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

# Create your models here.

class Prioridad(models.Model):
	idpri  =  models.AutoField(primary_key = True)
	prioridad = models.CharField(max_length = 15)
	def __unicode__(self):
		return self.prioridad

class Estatus(models.Model):
	idest  =  models.AutoField(primary_key = True)
	estatus = models.CharField(max_length = 100)
	def __unicode__(self):
		return self.estatus

class Acceso(models.Model):
	idacc  =  models.AutoField(primary_key = True)
	acceso = models.CharField(max_length = 100)
	def __unicode__(self):
		return self.acceso

class Tecnologia(models.Model):
	idtec  =  models.AutoField(primary_key = True)
	tecnologia = models.CharField(max_length = 100)
	def __unicode__(self):
		return self.tecnologia

class Proceder(models.Model):
	idpro  =  models.AutoField(primary_key = True)
	proceder = models.CharField(max_length = 100)
	def __unicode__(self):
		return self.proceder

class ClientesBit(models.Model):
	idcli  =  models.AutoField(primary_key = True)
	cliente = models.CharField(max_length = 100)
	logo = models.ImageField(upload_to='upload/bitacora/clientes/logo/')
	carousel = models.ImageField(upload_to='upload/bitacora/clientes/carousel/')
	def __unicode__(self):
		return self.cliente

class Nivel(models.Model):
	idniv  =  models.AutoField(primary_key = True)
	nivel = models.CharField(max_length = 25)
	def __unicode__(self):
		return self.nivel

"""class UserBit(models.Model):
        user = models.ForeignKey(User, unique=True)
	idniv = models.ForeignKey(Nivel)
	bitacora = models.BooleanField(default=True)
	def __unicode__(self):
		return self.user.username"""

class UserBit(User):
	idniv = models.ForeignKey(Nivel,null=True,blank=True)
	def __unicode__(self):
		return self.username

class Bitacora(models.Model):
    idbit =  models.AutoField(primary_key = True)
    creado = models.ForeignKey(UserBit,related_name='creador')
    im = models.CharField(_('IM'),max_length=15)
    idcli = models.ForeignKey(ClientesBit)
    localidad = models.CharField(_('Localidad'),max_length=100,null=True,blank=True)
    desc = models.TextField(_('Descripcion'),null=True,blank=True)
    idpri = models.ForeignKey(Prioridad)
    idest = models.ForeignKey(Estatus)
    idacc = models.ForeignKey(Acceso)
    idtec = models.ForeignKey(Tecnologia)
    idpro = models.ForeignKey(Proceder)
    #comentario = models.CharField(_('Ultimo comentario'),max_length=100,null=True,blank=True)
    idpri = models.ForeignKey(Prioridad)

    #accion = models.CharField(_('Acciones a Seguir'),max_length=100,null=True,blank=True)

    asignado = models.ForeignKey(UserBit,related_name='asignado',
					null=True,blank=True)
    ultimo = models.ForeignKey(UserBit,related_name='ultimo',
					null=True,blank=True)
    activo = models.ForeignKey(UserBit,related_name='Activo',
					null=True,blank=True)
    cerrado = models.NullBooleanField()
    fecha = models.DateField(_('Fecha creado'),
					auto_now_add=True, blank=True)
    hora = models.TimeField(_('Hora creado'),
					auto_now_add=True, blank=True)
    fecha_act = models.DateField(_('Fecha creado'),
					 null=True,blank=True)
    hora_act = models.TimeField(_('Hora creado'),
					 null=True,blank=True)
    fecha_mod = models.DateField(_('Fecha modificado'),
					null=True,blank=True)
    hora_mod = models.TimeField(_('Hora modificado'),
					null=True,blank=True)


class Ventana(models.Model):
    idven = models.AutoField(primary_key = True)
    idbit = models.ForeignKey(Bitacora)
    user = models.ForeignKey(UserBit)
    desc = models.TextField(_('Descripcion'),
					null=True,blank=True)
    fecha = models.DateField(_('Fecha modificado'),
					null=True,blank=True)
    hora = models.TimeField(_('Hora modificado'),
					null=True,blank=True)
