from django import forms
from django.forms import ModelForm
from ejercicio.bitacora.models import *

class UserBitRegForm(ModelForm):
     passw = forms.CharField(widget=forms.PasswordInput)
     check = forms.CharField(widget=forms.PasswordInput)
     class Meta:
          model = UserBit
          fields = ('first_name', 'last_name', 'username', 'email',)
          exclude = ('is_staff', 'is_active', 'password', 'date_joined', 'last_login')



class BitacoraAddForm(ModelForm):
    class Meta:
          model = Bitacora
          exclude = ( 'asignado', 'ultimo', 'activo', 'cerrado', 'fecha_mod', 'hora_mod')
    #creado = forms.CharField(widget=forms.HiddenInput())
