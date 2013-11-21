# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from axtel.quiz.models import *
from axtel.quiz.forms import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from datetime import datetime

######### Clave ##########
import random
import string


import base64
import uuid


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

@login_required
@user_passes_test(lambda u: u.is_staff)
def add(request):
    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	quiz = post['quiz']    
    	codigo = id_generator()
	#codigo = "prueba"
    	print "clave:", codigo
	duck = True
	while duck:
	    
		Qu = Quiz.objects.filter(codigo=codigo)
		if not Qu and quiz !="":
		    Q = Quiz(quiz=quiz,codigo=codigo)
		    Q.save()
		    duck = False
		    print "Guardo"
		else:
		    codigo = id_generator()
		    print "cambio de Clave"

    quiz = Quiz.objects.all()
    claves = Clave.objects.all()
    clave = []
    for c in claves:
	clave.append(int(c.idqui.idqui))
    return render_to_response("quiz/add.html",{'quiz':quiz,'clave':clave},context_instance=RequestContext(request))




@login_required
@user_passes_test(lambda u: u.is_staff)
def add_pregunta(request):
    if request.method == 'GET':
    	get = request.GET.copy()
    	idqui = get['idqui']

    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	idqui = post['idqui']    
	pregunta = post['pregunta']
	if pregunta != "":
	    P = Pregunta(idqui_id=idqui,pregunta=pregunta)
	    P.save()

    quiz = Quiz.objects.get(idqui=idqui)
    preguntas = Pregunta.objects.filter(idqui=idqui)
    return render_to_response("quiz/add_pregunta.html",{'quiz':quiz,'preguntas':preguntas})

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_respuesta(request):
    if request.method == 'GET':
    	get = request.GET.copy()
    	idpre = get['idpre']

    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	idpre = post['idpre']    
	respuesta = post['respuesta']
	if respuesta != "":
	    R = Respuesta(idpre_id=idpre,respuesta=respuesta)
	    R.save()

    preg = Pregunta.objects.get(idpre=idpre)
    respuestas = Respuesta.objects.filter(idpre=idpre)
    return render_to_response("quiz/add_respuesta.html",{'preg':preg,'respuestas':respuestas})

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_clave(request):
    if request.method == 'GET':
    	get = request.GET.copy()
    	idqui = get['idqui']

    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	idqui = post['idqui'] 	
    	preg = Pregunta.objects.filter(idqui=idqui)	
	clave=""
	for p in preg:
	    
	    idpre = post['preg_'+str(p.idpre)]   
	    clave+= str(p.idpre) + ":" + str(idpre) + '|'
	clave = clave[:-1]
	try:
	    C = Clave.objects.get(idqui=idqui)
	    C.clave = clave
	    C.save()
	except:
	    C = Clave(idqui_id=idqui,clave=clave)
	    C.save()

    preg = Pregunta.objects.filter(idqui=idqui)
    quiz = Quiz.objects.get(idqui=idqui)
    list_id = preg.values_list("idpre", flat=True)
    #tipo = Tipos.objects.filter(idtipo__in=list_id)

    respuestas = Respuesta.objects.filter(idpre__in=list_id)

    data = {'preguntas':preg,'respuestas':respuestas,'quiz':quiz}

    try:
    	c = Clave.objects.get(idqui=idqui)
    	cl = str(c.clave).split("|")
    	clave = []
    	print cl
    	for r in cl:
	    
	    print r,' ' , type(r), ' ' 
	    cla = r.split(":")[-1]
	    print cla, ' ' , type(cla)
	    clave.append(int(cla))
    	data['clave'] = clave
    except:
	pass

    return render_to_response("quiz/add_clave.html",data)


def contestar(request):
    if request.method == 'GET':
    	get = request.GET.copy()
    	idqui = get['idqui']

    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	codigo = post['codigo'] 

    try:
	Q = Quiz.objects.get(codigo=codigo)
	idqui = Q.idqui
    	preg = Pregunta.objects.filter(idqui=idqui)
    	quiz = Quiz.objects.get(idqui=idqui)
    	list_id = preg.values_list("idpre", flat=True)
    	#tipo = Tipos.objects.filter(idtipo__in=list_id)

    	respuestas = Respuesta.objects.filter(idpre__in=list_id)

    	data = {'preguntas':preg,'respuestas':respuestas,'quiz':quiz}
    	return render_to_response("quiz/contestar.html",data)
    except Quiz.DoesNotExist:
	mensaje = "No se ha encontrado ningun Ex&aacute;men con el codigo <b>"+str(codigo)+"</b>"
	return render_to_response("quiz/index.html",{'mensaje':mensaje})

def respuestas(request):
    if request.method == "POST":
        post = request.POST.copy()
    	idqui = post['idqui']	
    	nombre = post['nombre']
    	#noemp = post['noemp']

    	preg = Pregunta.objects.filter(idqui=idqui)
	claves = Clave.objects.get(idqui=idqui).clave

	cla = claves.split("|")
	clave = {}
	for c in cla:
	    cl = c.split(":")
	    clave[int(cl[0])] = int(cl[1])

	respuesta=""
	aciertos = 0
	errores = 0
	print clave
	for p in preg:
	    print p
	    idpre = int(post['preg_'+str(p.idpre)])
	    print idpre
	    respuesta+= str(p.idpre) + ":" + str(idpre) + '|'
	    #print int(idpre) , ' ', clave[int(idpre)]
	    c = clave[p.idpre]
	    if idpre == c:
		aciertos += 1   
	    else:
		errores += 1

	calif =  (float(aciertos) / float(aciertos + errores)) * 100
	respuesta = respuesta[:-1]
	R = Resultado(idqui_id=idqui,nombre=nombre,noemp=000000,clave=respuesta,aciertos=aciertos,errores=errores,calif=calif)
	R.save()

    return render_to_response("quiz/fin.html",{'r':R})
    #return HttpResponseRedirect('/axtel/quiz/fin/')
	
@login_required
@user_passes_test(lambda u: u.is_staff)
def resultados(request):
    if request.method == 'GET':
    	get = request.GET.copy()
    	idqui = get['idqui']

    resultados = Resultado.objects.filter(idqui=idqui)
    quiz = Quiz.objects.get(idqui=idqui)
    return render_to_response("quiz/resultados.html",{'resultados':resultados,'quiz':quiz})


def index(request):
    return render_to_response("quiz/index.html")

def fin(request):
    return render_to_response("quiz/fin.html")

@login_required
@user_passes_test(lambda u: u.is_staff)
def del_quiz(request):
    if request.method == "POST":
        post = request.POST.copy()
    	idqui = post['idqui']

	Q = Quiz.objects.get(idqui=idqui)
	Q.delete()

    return HttpResponseRedirect('/axtel/quiz/add/')

@login_required
@user_passes_test(lambda u: u.is_staff)
def del_pregunta(request):
    if request.method == "POST":
        post = request.POST.copy()
    	idpre = post['idpre']	
        idqui = Pregunta.objects.get(idpre=idpre).idqui.idqui
	P = Pregunta.objects.get(idpre=idpre)
	P.delete()

    return HttpResponseRedirect('/axtel/quiz/add_pregunta/?idqui=%s' % idqui)  
    #return render_to_response("quiz/add_pregunta.html",{'quiz':quiz,'preguntas':preguntas})

@login_required
@user_passes_test(lambda u: u.is_staff)
def del_respuesta(request):
    if request.method == "POST":
        post = request.POST.copy()
    	idres = post['idres']	
        Re = Respuesta.objects.get(idres=idres)
	idpre = Re.idpre.idpre
	R = Respuesta.objects.get(idres=idres)
	R.delete()

    return HttpResponseRedirect('/axtel/quiz/add_respuesta/?idpre=%s' % idpre)    
    #return render_to_response("quiz/add_respuesta.html",{'preg':preg,'respuestas':respuestas})

@login_required
@user_passes_test(lambda u: u.is_staff)
def detalles(request):
    if request.method == "POST":
        post = request.POST.copy()
    	idcla = post['idcla']	
	res = Resultado.objects.get(idcla=idcla)

    idqui = res.idqui.idqui
    preg = Pregunta.objects.filter(idqui=idqui)
    quiz = Quiz.objects.get(idqui=idqui)
    list_id = preg.values_list("idpre", flat=True)
    #tipo = Tipos.objects.filter(idtipo__in=list_id)

    respuestas = Respuesta.objects.filter(idpre__in=list_id)

    data = {'preguntas':preg,'respuestas':respuestas,'quiz':quiz,'datos':res}


    try:
    	c = Clave.objects.get(idqui=res.idqui.idqui)
    	cl = str(c.clave).split("|")
    	clave = []
    	print cl
    	for r in cl:
	    
	    print r,' ' , type(r), ' ' 
	    cla = r.split(":")[-1]
	    print cla, ' ' , type(cla)
	    clave.append(int(cla))
    	data['clave'] = clave
    except:
	pass

    try:
    	cl = str(res.clave).split("|")
    	clave2 = []
	pregun = []
    	print cl
    	for r in cl:
	    
	    print r,' ' , type(r), ' ' 
	    cla = r.split(":")[-1]
	    pre = r.split(":")[0]
	    
	    pregun.append(int(pre))

	    print cla, ' ' , type(cla)
	    clave2.append(int(cla))

	    

    	data['res'] = clave2
    except:
	pass
    
    check = {}
    for n in range(len(pregun)):
	if clave[n] == clave2[n]:
	    check[pregun[n]] = True
	else:
	    check[pregun[n]] = False
    data['check'] = check
    return render_to_response("quiz/detalles.html",data)

"""def nuevo(request):
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
		    obj.is_active = 0
		    obj.idniv_id = 1
		    obj.save()
        	    #form.save()


            	return HttpResponseRedirect('/axtel/bitacora/')
	else:
	    mensaje = "Contrasenas incorrectas"
	    usuarios = UserBit2.objects.all()
            form = UserBitRegForm()
	    return render_to_response("bitacora/nuevo.html",{'form':form,'usuarios':usuarios,'mensaje':mensaje})

    usuarios = UserBit2.objects.all()
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
		u=UserBit2.objects.get(user_ptr=user.id)
		if u.idniv.idniv == 2:
	      	    request.session['nivel']= True
		else:
		    request.session['nivel']= False

	        return HttpResponseRedirect('/axtel/bitacora/')
		#return render_to_response("bitacora/index.html",{'mensaje':mensaje},context_instance=RequestContext(request))
            else:
            	mensaje= "Tu cuenta no ha sido activada."
    	        return render_to_response("bitacora/index.html",{'mensaje':mensaje},context_instance=RequestContext(request))
	else:
            mensaje= "Usuario y contrase&ntilde;a incorrectos."
    	    return render_to_response("bitacora/index.html",{'mensaje':mensaje},context_instance=RequestContext(request))
    request.notifications.add('Hello world.')
    request.notifications.success('Profile details updated.')
    request.notifications.warning('Your account expires in three days.')
    request.notifications.error('Document deleted.')
    return render_to_response("bitacora/index.html",context_instance=RequestContext(request))

def bitacora(request):
    bitacora = Bitacora.objects.filter(cerrado__isnull=True)

    return render_to_response("bitacora/bitacora.html",{'bitacora':bitacora},context_instance=RequestContext(request))

def notify(request):
    get = request.GET.copy()
    user_id = get['id']
    total = len(Bitacora.objects.filter(cerrado__isnull=True))
    abiertos = len(Bitacora.objects.filter(cerrado__isnull=True).filter(activo=user_id))
    asignados = len(Bitacora.objects.filter(cerrado__isnull=True).filter(asignado=user_id))
    cerrados = len(Bitacora.objects.filter(cerrado__isnull=False))
    return render_to_response("bitacora/notify.html",{'total':total,'abiertos':abiertos,'asignados':asignados,'cerrados':cerrados},context_instance=RequestContext(request))

def index2(request):
    return render_to_response("bitacora/index2.html",context_instance=RequestContext(request))
      

def index3(request):
    return render_to_response("bitacora/index3.html",context_instance=RequestContext(request))     

@login_required
def add(request):
    if request.method == 'POST': # If the form has been submitted...
        form = BitacoraAddForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
       	    # Process the data in form.cleaned_data
	    #obj = form.save(commit=False)
	    #obj.set_password(passw)
	    #obj.save()
       	    form.save()

	    return HttpResponseRedirect('/axtel/bitacora/')
	
    bitacora = Bitacora.objects.all()
    u=UserBit2.objects.get(user_ptr=request.user.id)
    form = BitacoraAddForm(initial={'creado':u.user_ptr_id})
    return render_to_response("bitacora/add.html",{'form':form,'bitacora':bitacora},context_instance=RequestContext(request))

def update(request):
    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	idbit = post['idbit']
	print "idbit..", idbit
	b = Bitacora.objects.get(idbit=idbit)
	u=UserBit2.objects.get(user_ptr=request.user.id)
	print "sesion user id ...", request.session['user_id']
	print "sesion user...", request.user
	print "usuario...",u.user_ptr_id,"uuuuuuu... ", u
	if b.activo and b.activo != u:
	    return HttpResponseRedirect('/axtel/bitacora/')
	b.activo_id = u
	b.save()
	prioridad = Prioridad.objects.all()
	proceder = Proceder.objects.all()
	estatus = Estatus.objects.all()
	acceso = Acceso.objects.all()
        users=UserBit2.objects.filter(is_active=1)
	data = {'b':b,'prioridad':prioridad,'estatus':estatus,'proceder':proceder,'acceso':acceso,'u':u,'users':users}
	return render_to_response("bitacora/update.html",data,context_instance=RequestContext(request))

def tomar(request):
    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	idbit = post['idbit']
	print "idbit..", idbit
	b = Bitacora.objects.get(idbit=idbit)
	u=UserBit2.objects.get(user_ptr=request.user.id)
	print "sesion user id ...", request.session['user_id']
	print "sesion user...", request.user
	print "usuario...",u.user_ptr_id,"uuuuuuu... ", u
	if b.activo and b.activo != u:
	    return HttpResponseRedirect('/axtel/bitacora/')
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
	return HttpResponseRedirect('/axtel/bitacora/')

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
	comentario = post['comentario']
	accion = post['accion']
	print "idbit..", idbit
	b = Bitacora.objects.get(idbit=idbit)
	u=UserBit2.objects.get(user_ptr=request.user.id)
	print "sesion user id ...", request.session['user_id']
	print "sesion user...", request.user
	print "usuario...",u.user_ptr_id,"uuuuuuu... ", u
	b.ultimo_u = u
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
	    re=UserBit2.objects.get(user_ptr=reasignar)

	    b.asignado_id = re	
        except:
	    pass
	b.comentario = comentario
	b.accion = accion
	b.fecha_mod = datetime.now()
	b.hora_mod = datetime.now()
	try:
		b.cerrado = cerrado
	except:
		pass
	b.save()
	return HttpResponseRedirect('/axtel/bitacora/')

def logout(request):
    request.session.flush()

    return HttpResponseRedirect('/axtel/bitacora/')

####### MI PRIMER DECORADOR ##############

# Pasa si existe la variable de sesion 'nivel'

def nivel_ilimitado(view):
    def bad(request,*args,**kargs):
	if request.session['nivel']:
	    return view(request,*args,**kargs)
	else:
	    return HttpResponseRedirect('/axtel/bitacora/')    
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
	        u = UserBit2.objects.get(user_ptr=asignar)
	    	B = Bitacora.objects.get(idbit=b.idbit)
	    	B.asignado_id = u
	    	B.save()
	
	return HttpResponseRedirect('/axtel/bitacora/asignar/')
      users=UserBit2.objects.filter(is_active=1)

      return render_to_response("bitacora/asignar.html",{'bitacora':bitacora,'users':users},context_instance=RequestContext(request))


@nivel_ilimitado
def activar(request):
    if request.method == 'POST': 
	array = request.POST.getlist('array')   

	for a in array:
	    u = UserBit2.objects.get(user_ptr=a)
	    u.is_active = 1
	    u.save()
	
	return HttpResponseRedirect('/axtel/bitacora/activar/')
    users=UserBit2.objects.filter(user_ptr__is_active=0)

    return render_to_response("bitacora/activar.html",{'bitacora':bitacora,'users':users},context_instance=RequestContext(request))

@nivel_ilimitado
def privilegios(request):
    users=UserBit2.objects.all()
    if request.method == 'POST': 
	#array = request.POST.getlist('array')   
	post = request.POST.copy()
	for u in users:
	    nivel = int(post['nivel_'+str(u.id)])
	    us = UserBit2.objects.get(user_ptr=u.id)
	    us.idniv_id = nivel
	    us.save()
	
	return HttpResponseRedirect('/axtel/bitacora/privilegios/')
    nivel=Nivel.objects.all()

    return render_to_response("bitacora/privilegios.html",{'nivel':nivel,'users':users},context_instance=RequestContext(request))

################### Refresh de Bitacora onclick ######################



def window_notification(request):
    return render_to_response("bitacora/window-notification.html",context_instance=RequestContext(request))

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
    return render_to_response("bitacora/bitacora.html",{'bitacora':bitacora},context_instance=RequestContext(request))


def abiertos(request):
    get = request.GET.copy()
    user_id = get['id']
    bitacora = Bitacora.objects.filter(cerrado__isnull=True).filter(activo=user_id)
    return render_to_response("bitacora/bitacora.html",{'bitacora':bitacora},context_instance=RequestContext(request))

def eliminar(request):
    if request.method == 'POST': 
	array = request.POST.getlist('array')   

	for a in array:
	    B = Bitacora.objects.get(idbit=a)
	    B.delete()

	return HttpResponseRedirect('/axtel/bitacora/')
    bitacora = Bitacora.objects.filter(cerrado__isnull=False).order_by('fecha_mod')
    return render_to_response("bitacora/eliminar.html",{'bitacora':bitacora},context_instance=RequestContext(request))

def perfil(request):
    if request.method == 'POST': # If the form has been submitted...
        post = request.POST.copy()
	user_id = post['user_id']
	first_name = post['first_name']
	last_name = post['last_name']
	email = post['email']
	#oldpass = post['oldpass']
	newpass = post['newpass']
	check = post['check']
        U = User.objects.get(id=user_id)
	U.first_name = first_name
	U.last_name = last_name
	U.email = email
	print "pass", U.password
	if newpass == check:
		U.set_password(newpass)
	U.save()
	return HttpResponseRedirect('/bitacora/perfil/')

    #userbit=UserBit2.objects.get(user_ptr=request.user.id)
    return render_to_response("bitacora/perfil.html",context_instance=RequestContext(request))"""
