# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from ejercicio.bitacora.models import *
from ejercicio.bitacora.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime,timedelta, date
import time

today = datetime.now()


def nuevo(request):
    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	passw = post['passw']
	check = post['check']
	if passw == check:

	        form = UserBitRegForm(request.POST) # A form bound to the POST data
	        if form.is_valid(): # All validation rules pass
        	    # Process the data in form.cleaned_data
		    obj = form.save(commit=False)
		    obj.set_password(passw)
		    obj.is_active = 1
		    obj.idniv_id = 1
		    obj.save()
        	    """form.save()"""


            	return HttpResponseRedirect('/bitacora/')
	else:
	    mensaje = "Contrasenas incorrectas"
	    usuarios = UserBit.objects.all()
            form = UserBitRegForm()
	    return render_to_response("bitacora/nuevo.html",{'form':form,'usuarios':usuarios,'mensaje':mensaje})

    usuarios = UserBit.objects.all()
    form = UserBitRegForm()
    return render_to_response("bitacora/nuevo.html",{'form':form,'usuarios':usuarios})

def index(request):
    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	#cliente = int(get['cliente'])
	usuario = post['usuario']
	contra = post['contra']
	
	user = authenticate(username=usuario, password=contra)
	if user is not None:
    	    if user.is_active:
        	mensaje= "You provided a correct username and password!"
		request.session['user_id'] = user.id
                login(request, user)
		u=UserBit.objects.get(user_ptr=user.id)
		if u.idniv.idniv == 2:
	      	    request.session['nivel']= True
		else:
		    request.session['nivel']= False

	        return HttpResponseRedirect('/bitacora/')
		#return render_to_response("bitacora/index.html",{'mensaje':mensaje},context_instance=RequestContext(request))
            else:
            	mensaje= "Tu cuenta no ha sido activada."
    	        return render_to_response("bitacora/index.html",{'mensaje':mensaje},context_instance=RequestContext(request))
	else:
            mensaje= "Usuario y contrase&ntilde;a incorrectos."
    	    return render_to_response("bitacora/index.html",{'mensaje':mensaje},context_instance=RequestContext(request))

    return render_to_response("bitacora/index.html",context_instance=RequestContext(request))

def bitacora(request):
    bitacora = Bitacora.objects.filter(cerrado__isnull=True)
    list_id = bitacora.values_list("idbit", flat=True)
    ventana = Ventana.objects.filter(idbit__in=list_id)
    
    bita = Bitacora.objects.filter(cerrado__isnull=True,hora_act__isnull=False)
    for b in bita:
	start = datetime(b.fecha_act.year,b.fecha_act.month,b.fecha_act.day,b.hora_act.hour,b.hora_act.minute,b.hora_act.second)
	now = datetime.now()
	delta = now - start	
	#print delta
	if delta > timedelta(hours=2):
	    b.hora_act = None
	    b.fecha_act = None
	    b.activo = None
	    b.save()

    return render_to_response("bitacora/bitacora.html",{'bitacora':bitacora,'ventana':ventana},context_instance=RequestContext(request))

def notify(request):
    get = request.GET.copy()
    user_id = get['id']
    total = len(Bitacora.objects.filter(cerrado__isnull=True))
    abiertos = len(Bitacora.objects.filter(cerrado__isnull=True).filter(activo=user_id))
    asignados = len(Bitacora.objects.filter(cerrado__isnull=True).filter(asignado=user_id))
    my_filter = {}
    my_filter['cerrado__isnull'] = False

    u=UserBit.objects.get(user_ptr=request.user.id)

    if u.idniv.idniv == 1:
	my_filter['creado'] = u.user_ptr


    cerrados = len(Bitacora.objects.filter(**my_filter))
    activar = len(UserBit.objects.filter(is_active=0))
    return render_to_response("bitacora/notify.html",{'total':total,'abiertos':abiertos,'asignados':asignados,'cerrados':cerrados,'activar':activar},context_instance=RequestContext(request))

def index2(request):
    return render_to_response("bitacora/index2.html",context_instance=RequestContext(request))
      

def index3(request):
    return render_to_response("bitacora/index3.html",context_instance=RequestContext(request))     

#@login_required
def add(request):
    if request.method == 'POST': # If the form has been submitted...
        form = BitacoraAddForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
       	    # Process the data in form.cleaned_data
	    #obj = form.save(commit=False)
	    #obj.set_password(passw)
	    #obj.save()
       	    form.save()

	    return HttpResponseRedirect('/bitacora/')
	
    bitacora = Bitacora.objects.all()
    u=UserBit.objects.get(user_ptr=request.user.id)
    form = BitacoraAddForm(initial={'creado':u.user_ptr_id})
    return render_to_response("bitacora/add.html",{'form':form,'bitacora':bitacora},context_instance=RequestContext(request))

def update(request):
    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	idbit = post['idbit']
	print "idbit..", idbit
	b = Bitacora.objects.get(idbit=idbit)
	u=UserBit.objects.get(user_ptr=request.user.id)
	print "sesion user id ...", request.session['user_id']
	print "sesion user...", request.user
	print "usuario...",u.user_ptr_id,"uuuuuuu... ", u
	if b.activo and b.activo != u:
	    return HttpResponseRedirect('/bitacora/')
	b.activo_id = u
	b.fecha_act = datetime.now()
	b.hora_act = datetime.now()
	b.save()
	prioridad = Prioridad.objects.all()
	proceder = Proceder.objects.all()
	estatus = Estatus.objects.all()
	acceso = Acceso.objects.all()
        users=UserBit.objects.filter(is_active=1)
	data = {'b':b,'prioridad':prioridad,'estatus':estatus,'proceder':proceder,'acceso':acceso,'u':u,'users':users}
	return render_to_response("bitacora/update.html",data,context_instance=RequestContext(request))

def tomar(request):
    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	idbit = post['idbit']
	print "idbit..", idbit
	b = Bitacora.objects.get(idbit=idbit)
	u=UserBit.objects.get(user_ptr=request.user.id)
	print "sesion user id ...", request.session['user_id']
	print "sesion user...", request.user
	print "usuario...",u.user_ptr_id,"uuuuuuu... ", u
	if b.activo and b.activo != u:
	    return HttpResponseRedirect('/bitacora/')
	b.activo_id = u
	b.asignado_id = u

	b.save()
	prioridad = Prioridad.objects.all()
	proceder = Proceder.objects.all()
	estatus = Estatus.objects.all()
	acceso = Acceso.objects.all()
	data = {'b':b,'prioridad':prioridad,'estatus':estatus,'proceder':proceder,'acceso':acceso,'u':u}
	return render_to_response("bitacora/update.html",data,context_instance=RequestContext(request))

def reasignar(request):
    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	idbit = post['idbit']
        reasignar = int(post['reasignar_'+str(idbit)])
	b = Bitacora.objects.get(idbit=idbit)
	b.asignado_id = reasignar
	b.save()
	return HttpResponseRedirect('/bitacora/')

def save(request):
    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	idbit = post['idbit']
	idpri = int(post['idpri'])
	idpro = int(post['idpro'])
	idest = int(post['idest'])
	idacc = int(post['idacc'])

	try:
	        reasignar = int(post['reasignar'])
	except:
		pass

	try:
		cerrado = post['cerrado']
	except:
		pass
	desc = post['desc']

	print "idbit..", idbit
	b = Bitacora.objects.get(idbit=idbit)



	u=UserBit.objects.get(user_ptr=request.user.id)


	if b.activo == u:
	 print "sesion user id ...", request.session['user_id']
	 print "sesion user...", request.user
	 print "usuario...",u.user_ptr_id,"uuuuuuu... ", u
	 b.ultimo_id = u
	 b.activo = None
	 b.idpri_id = idpri
	 b.idpro_id = idpro
	 b.idest_id = idest
	 b.idacc_id = idacc
	 b.desc = desc
	 try:
	  if reasignar != 0 and reasignar == 9999:
	      b.asignado = None
	  elif reasignar !=0:
	    re=UserBit.objects.get(user_ptr=reasignar)

	    b.asignado_id = re	
         except:
	    pass

	 b.fecha_mod = datetime.now()
	 b.hora_mod = datetime.now()
	 b.fecha_act = None
	 b.hora_act = None
	 try:
		b.cerrado = cerrado
	 except:
		pass
	
	 b.save()
	return HttpResponseRedirect('/bitacora/')

def logout(request):
    request.session.flush()

    return HttpResponseRedirect('/bitacora/')

####### MI PRIMER DECORADOR ##############

# Pasa si existe la variable de sesion 'nivel'

def nivel_ilimitado(view):
    def bad(request,*args,**kargs):
	if request.session['nivel']:
	    return view(request,*args,**kargs)
	else:
	    return HttpResponseRedirect('/bitacora/')    
    return bad

################################################


@nivel_ilimitado
def asignar(request):

      bitacora = Bitacora.objects.filter(cerrado__isnull=True).filter(asignado__isnull=True,activo__isnull=True)
      if request.method == 'POST': 
	post = request.POST.copy()
	for b in bitacora:
	    asignar = int(post['asignar_'+str(b.idbit)])

	    if asignar != 0:
	        u = UserBit.objects.get(user_ptr=asignar)
	    	B = Bitacora.objects.get(idbit=b.idbit)
	    	B.asignado_id = u
	    	B.save()
	
	return HttpResponseRedirect('/bitacora/asignar/')
      users=UserBit.objects.filter(is_active=1)

      return render_to_response("bitacora/asignar.html",{'bitacora':bitacora,'users':users},context_instance=RequestContext(request))


@nivel_ilimitado
def activar(request):
    if request.method == 'POST': 
	array = request.POST.getlist('array')   

	for a in array:
	    u = UserBit.objects.get(user_ptr=a)
	    u.is_active = 1
	    u.save()
	
	return HttpResponseRedirect('/bitacora/activar/')
    users=UserBit.objects.filter(user_ptr__is_active=0)

    return render_to_response("bitacora/activar.html",{'bitacora':bitacora,'users':users},context_instance=RequestContext(request))

@nivel_ilimitado
def privilegios(request):
    users=UserBit.objects.filter(is_active=1)
    if request.method == 'POST': 
	#array = request.POST.getlist('array')   
	post = request.POST.copy()
	for u in users:
	    nivel = int(post['nivel_'+str(u.id)])
	    us = UserBit.objects.get(user_ptr=u.id)
	    us.idniv_id = nivel
	    us.save()
	
	return HttpResponseRedirect('/bitacora/privilegios/')
    nivel=Nivel.objects.all()

    return render_to_response("bitacora/privilegios.html",{'nivel':nivel,'users':users},context_instance=RequestContext(request))

################### Refresh de Bitacora onclick ######################

def bitacora22(request):
    bitacora = Bitacora.objects.filter(cerrado__isnull=True)
    return render_to_response("bitacora/bitacora.html",{'bitacora':bitacora},context_instance=RequestContext(request))

def total(request):
    get = request.GET.copy()
    user_id = get['id']
    bitacora = Bitacora.objects.filter(cerrado__isnull=True)
    return render_to_response("bitacora/bitacora.html",{'bitacora':bitacora},context_instance=RequestContext(request))

def asignados(request):
    get = request.GET.copy()
    user_id = get['id']
    bitacora = Bitacora.objects.filter(cerrado__isnull=True).filter(asignado=user_id)
    list_id = bitacora.values_list("idbit", flat=True)
    ventana = Ventana.objects.filter(idbit__in=list_id)
    return render_to_response("bitacora/bitacora.html",{'bitacora':bitacora,'ventana':ventana},context_instance=RequestContext(request))


def abiertos(request):
    get = request.GET.copy()
    user_id = get['id']
    bitacora = Bitacora.objects.filter(cerrado__isnull=True).filter(activo=user_id)
    list_id = bitacora.values_list("idbit", flat=True)
    ventana = Ventana.objects.filter(idbit__in=list_id)
    return render_to_response("bitacora/bitacora.html",{'bitacora':bitacora,'ventana':ventana},context_instance=RequestContext(request))



def eliminar(request):
    if request.method == 'POST': 
	array = request.POST.getlist('array')   

	for a in array:
	    B = Bitacora.objects.get(idbit=a)
	    B.delete()

	return HttpResponseRedirect('/bitacora/')

    my_filter = {}
    my_filter['cerrado__isnull'] = False

    u=UserBit.objects.get(user_ptr=request.user.id)

    if u.idniv.idniv == 1:
	my_filter['creado'] = u.user_ptr

    bitacora = Bitacora.objects.filter(**my_filter).order_by('fecha_mod')
    return render_to_response("bitacora/eliminar.html",{'bitacora':bitacora},context_instance=RequestContext(request))

def perfil(request):
    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	user_id = post['user_id']
	first_name = post['first_name']
	last_name = post['last_name']
	email = post['email']
	newpass = post['newpass']
	check = post['check']
        U = User.objects.get(id=user_id)
	U.first_name = first_name
	U.last_name = last_name
	U.email = email
	if not newpass and not check:
		mensaje = "La contrase&ntilde;a no puede quedar en blanco, se realizaron los demas cambios"
	elif newpass == check:
		U.set_password(newpass)
		mensaje = "Cambio exitoso de contrase&ntilde;a "
	else:
		mensaje = "Las contrase&ntilde;as introducidas no son iguales"
	
	U.save()
	return render_to_response("bitacora/perfil.html",{'mensaje':mensaje},context_instance=RequestContext(request))

    #userbit=UserBit.objects.get(user_ptr=request.user.id)
    return render_to_response("bitacora/perfil.html",context_instance=RequestContext(request))


@nivel_ilimitado
def delete_user(request):
    users=UserBit.objects.all()
    if request.method == 'POST':
	array = request.POST.getlist('array')   

	for a in array:
	    ub = UserBit.objects.get(user_ptr=a)
	    ub.delete()

    return render_to_response("bitacora/delete_user.html",{'users':users},context_instance=RequestContext(request))


def detalles(request):
    get = request.GET.copy()
    idbit = get['idbit']
    if request.method == 'POST':
	post = request.POST.copy()
	fecha = post['fecha']
	hora = post['hora']	
	desc = post['desc']
        if fecha != "" or hora != "" or desc != "":
	      try:
	    	V = Ventana.objects.get(idbit=idbit)
		V.fecha = fecha
	 	V.hora = hora
		V.desc = desc
		V.save()
	      except:
		u=UserBit.objects.get(user_ptr=request.user.id)
		V=Ventana(idbit_id=idbit,user_id=u.id,fecha=fecha,hora=hora,desc=desc)
		V.save()
    data = {}
    try:
    	v = Ventana.objects.get(idbit=idbit)
	data['v'] = v
    except:
	pass
    b = Bitacora.objects.get(idbit=idbit)
    data['b'] = b
    return render_to_response("bitacora/detalles.html",data,context_instance=RequestContext(request))

def recuperar(request):
        get = request.GET.copy()
        idbit = get['idbit']
	B = Bitacora.objects.get(idbit=idbit)
	B.cerrado = None
	B.save()
	return HttpResponseRedirect('/bitacora/')


def ventana(request):
    bitacora = Bitacora.objects.filter(cerrado__isnull=True)
    if request.method == 'POST':
        post = request.POST.copy()
	u=UserBit.objects.get(user_ptr=request.user.id)
	for b in bitacora:
	    fecha = post['fecha_'+str(b.idbit)]
	    hora = post['hora_'+str(b.idbit)]	
	    desc = post['desc_'+str(b.idbit)]
	    if fecha != "" or hora != "" or desc != "":
	      try:
	    	V = Ventana.objects.get(idbit=b.idbit)
		V.fecha = fecha
	 	V.hora = hora
		V.desc = desc
		V.save()
	      except:
		V=Ventana(idbit_id=b.idbit,user_id=u.id,fecha=fecha,hora=hora,desc=desc)
		V.save()
	return HttpResponseRedirect('/bitacora/ventana/')
    ventana = Ventana.objects.all()
    return render_to_response("bitacora/ventana.html",{'bitacora':bitacora,'ventana':ventana},context_instance=RequestContext(request))


def window_notification(request):
    tiempos = {}
    hoy = date.today()
    notifications = Ventana.objects.filter(fecha=hoy)
    for n in notifications:

	fecha = datetime(n.fecha.year,n.fecha.month,n.fecha.day,n.hora.hour,n.hora.minute,n.hora.second)
	now = datetime.now()
	delta = fecha - now
	tiempos[n.idven] = int(delta.total_seconds())

    return render_to_response("bitacora/window-notification.html",{'notifications':notifications,'tiempos':tiempos},context_instance=RequestContext(request))

def eliminar_ventana(request):

    if request.method == 'POST':
        post = request.POST.copy()
	idbit= post['idbit']
        try:
	    B = Ventana.objects.get(idbit=idbit)
	    B.delete()
	except:
	    pass

    return HttpResponseRedirect('/bitacora/detalles?idbit=%s' % idbit)

