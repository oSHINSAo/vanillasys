# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from ejercicio.opindependencia.models import *
from ejercicio.opindependencia.forms import *
from ejercicio.opindependencia.tables  import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from datetime import datetime

from django.db.models import Q

######### Clave ##########
import random
import string


import base64
import uuid


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def index(request):

    attack2 = ClientesAttack.objects.filter(~Q(idsta=5))

    list_id = attack2.values_list("idcli", flat=True)

    list_idcla = attack2.values_list("idcla", flat=True)

    clientes = Clientes.objects.all()
    accion = Acciones.objects.all().order_by('-idacc')
    situacion = Situacion.objects.all().order_by('-idacc')
    attack = ClientesAttack.objects.all().order_by('-idcla')
    graficas = Graficas.objects.all().order_by('-idgra')
    no_menu = True

    #menu = Menu.objects.filter(user_id=request.user.id)


    browser = request.META['HTTP_USER_AGENT']

    return render_to_response("opindependencia/index.html",{'clientes':clientes,'accion':accion,'situacion':situacion,'attack':attack, 'graficas':graficas,'no_menu':no_menu,'browser':browser, 'list_id':list_id},
                              context_instance=RequestContext(request))



#@login_required
#@user_passes_test(lambda u: u.is_staff)
def add_status(request):

    if request.method == 'POST': # If the form has been submitted...
	post = request.POST.copy()
	status = post['status']    
	if status != "":
	    S = Status(status=status)
	    S.save()

    status = Status.objects.all()
    return render_to_response("opindependencia/add_status.html",{'status':status})

#@login_required
#@user_passes_test(lambda u: u.is_staff)
def add_tipo(request):

    if request.method == 'POST': # If the form has been submitted...
	post = request.POST.copy()
	tipo = post['tipo']    
	if tipo != "":
	    T = Tipo(tipo=tipo)
	    T.save()

    tipos = Tipo.objects.all()
    return render_to_response("opindependencia/add_tipos.html",{'tipos':tipos})


#@login_required
#@user_passes_test(lambda u: u.is_staff)
def add_cliente(request):

    if request.method == 'POST': # If the form has been submitted...
	post = request.POST.copy()
	cliente = post['cliente']   
	tipo = post['tipo']   
	if cliente != "" and tipo != "":
	    C = Clientes(cliente=cliente,tipo=tipo)
	    C.save()

    clientes = Clientes.objects.all()
    return render_to_response("opindependencia/add_cliente.html",{'clientes':clientes})

#@login_required
#@user_passes_test(lambda u: u.is_staff)
def add_accion(request):

    if request.method == 'POST': # If the form has been submitted...
	post = request.POST.copy()
	idcla = post['idcla']   
	accion = post['accion']   
	if idcla != "" and accion != "":
	    A = Acciones(idcla_id=idcla,accion=accion)
	    A.save()

    accion = Acciones.objects.all()
    attack = ClientesAttack.objects.all()
    return render_to_response("opindependencia/add_accion.html",{'accion':accion,'attack':attack})



#@login_required
#@user_passes_test(lambda u: u.is_staff)
def add_situacion(request):

    if request.method == 'POST': # If the form has been submitted...
	post = request.POST.copy()
	idcla = post['idcla']   
	situacion = post['situacion']   
	if idcla != "" and situacion != "":
	    S = Situacion(idcla_id=idcla,situacion=situacion)
	    S.save()

    situacion = Situacion.objects.all()
    attack = ClientesAttack.objects.all()
    return render_to_response("opindependencia/add_situacion.html",{'situacion':situacion,'attack':attack})

#@login_required
#@user_passes_test(lambda u: u.is_staff)
def add_attack(request):

    if request.method == 'POST': # If the form has been submitted...
	post = request.POST.copy()
	idcli = post['idcli']   
	idtip = post['idtip']   
	consecuencia = post['consecuencia']
	idsta = post['idsta']
	if idcli != "":
	    C = ClientesAttack(idcli_id=idcli,idtip_id=idtip,consecuencia=consecuencia,idsta_id=idsta)
	    C.save()
	    
	    accion = post['accion']
	    situacion = post['situacion']
	    if accion != "":
		A=Acciones(idcla_id=C.idcla,accion=accion)
		A.save()
	    if situacion != "":
		S=Situacion(idcla_id=C.idcla,situacion=situacion)
		S.save()
    	    try:
		image = request.FILES['image']
		G= Graficas(idcla_id=C.idcla,grafica=image)
		G.save()
	    except:
		pass
    #attack = ClientesAttack.objects.all()
    attack = ClientesAttack.objects.filter(~Q(idsta=5))
    clientes = Clientes.objects.all()
    status = Status.objects.all()
    tipos = Tipo.objects.all()
    return render_to_response("opindependencia/add_attack.html",{'clientes':clientes,'attack':attack, 'status':status, 'tipos':tipos})


#@login_required
#@user_passes_test(lambda u: u.is_staff)
def alcance(request):
    clientes = Clientes.objects.all()
    if request.method =="POST":
	b = []
	for c in clientes:
	    b.append(c.idcli)
	array = request.POST.getlist('array')
	for a in array:
	    b.remove(int(a))   
	for a in array:
    	    C = Clientes.objects.get(idcli=a)
	    C.peligro = True
	    C.save()
	for a in b:
    	    C = Clientes.objects.get(idcli=a)
	    C.peligro = False
	    C.save()
	return HttpResponseRedirect('/opindependencia/alcance/')

    return render_to_response("opindependencia/alcance.html",{'clientes':clientes})

def auto_attack(request):
    attack = ClientesAttack.objects.all().order_by('-idcla')
    return render_to_response("opindependencia/auto_attack.html",{'attack':attack})

def auto_twitter(request):
    return render_to_response("opindependencia/auto_twitter.html")

def auto_accion(request):
    accion = Acciones.objects.all().order_by('-idacc')
    return render_to_response("opindependencia/auto_accion.html",{'accion':accion})

def auto_situacion(request):
    situacion = Situacion.objects.all().order_by('-idacc')
    return render_to_response("opindependencia/auto_situacion.html",{'situacion':situacion})

def auto_graficas(request):
    graficas = Graficas.objects.all().order_by('-idgra')
    return render_to_response("opindependencia/auto_graficas.html",{'graficas':graficas})

def auto_clientes(request):
    clientes = Clientes.objects.all()
    attack2 = ClientesAttack.objects.filter(~Q(idsta=5))
    list_id = attack2.values_list("idcli", flat=True)
    return render_to_response("opindependencia/auto_clientes.html",{'clientes':clientes,'list_id':list_id})

def update(request):
   if request.method == 'POST': # If the form has been submitted...
	post = request.POST.copy()
	idcla = post['idcla']   
	idsta = post['idsta']  
	CA = ClientesAttack.objects.get(idcla=idcla)
	CA.idsta_id = idsta
	if idsta == 5:
	    CA.fecha_fin = datetime.now()
	    CA.hora_fin = datetime.now()
	CA.save()
	return HttpResponseRedirect('/opindependencia/add_attack/')

