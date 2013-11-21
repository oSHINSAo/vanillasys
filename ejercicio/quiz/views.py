# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from ejercicio.quiz.models import *
from ejercicio.quiz.forms import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from datetime import datetime

######### Clave ##########
import random
import string
import xlrd
import xlwt

import base64
import uuid


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

#@login_required
#@user_passes_test(lambda u: u.is_staff)
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




#@login_required
#@user_passes_test(lambda u: u.is_staff)
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

#@login_required
#@user_passes_test(lambda u: u.is_staff)
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

#@login_required
#@user_passes_test(lambda u: u.is_staff)
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
    #return HttpResponseRedirect('/quiz/fin/')
	
#@login_required
#@user_passes_test(lambda u: u.is_staff)
def resultados(request):
    if request.method == 'GET':
    	get = request.GET.copy()
    	idqui = get['idqui']

    resultados = Resultado.objects.filter(idqui=idqui).order_by('fecha')
    quiz = Quiz.objects.get(idqui=idqui)
    return render_to_response("quiz/resultados.html",{'resultados':resultados,'quiz':quiz})


def index(request):
    return render_to_response("quiz/index.html")

def fin(request):
    return render_to_response("quiz/fin.html")

#@login_required
#@user_passes_test(lambda u: u.is_staff)
def del_quiz(request):
    if request.method == "POST":
        post = request.POST.copy()
    	idqui = post['idqui']

	Q = Quiz.objects.get(idqui=idqui)
	Q.delete()

    return HttpResponseRedirect('/quiz/add/')

#@login_required
#@user_passes_test(lambda u: u.is_staff)
def del_pregunta(request):
    if request.method == "POST":
        post = request.POST.copy()
    	idpre = post['idpre']	
        idqui = Pregunta.objects.get(idpre=idpre).idqui.idqui
	P = Pregunta.objects.get(idpre=idpre)
	P.delete()

    return HttpResponseRedirect('/quiz/add_pregunta/?idqui=%s' % idqui)  
    #return render_to_response("quiz/add_pregunta.html",{'quiz':quiz,'preguntas':preguntas})

#@login_required
#@user_passes_test(lambda u: u.is_staff)
def del_respuesta(request):
    if request.method == "POST":
        post = request.POST.copy()
    	idres = post['idres']	
        Re = Respuesta.objects.get(idres=idres)
	idpre = Re.idpre.idpre
	R = Respuesta.objects.get(idres=idres)
	R.delete()

    return HttpResponseRedirect('/quiz/add_respuesta/?idpre=%s' % idpre)    
    #return render_to_response("quiz/add_respuesta.html",{'preg':preg,'respuestas':respuestas})

#@login_required
#@user_passes_test(lambda u: u.is_staff)
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

def ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return render_to_response("quiz/ip.html",{'ip':ip})

#@login_required
#@user_passes_test(lambda u: u.is_staff)
def excel_resultados(request):

    start = datetime.now()

    if request.method =="POST": 
    	post = request.POST.copy()
    	idqui = int(post['idqui'])
    	#ano = int(post['ano'])

	quiz = Quiz.objects.get(idqui=idqui)
	res = Resultado.objects.filter(idqui=idqui).order_by('fecha')
	



	book = xlwt.Workbook(encoding='utf8')
	sheet = book.add_sheet('untitled')

	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

	first_col = sheet.col(0)
	first_col.width = 256 * 30              # 20 characters wide (-ish)
	first_col = sheet.col(1)
	first_col.width = 256 * 15
 	first_col = sheet.col(2)
	first_col.width = 256 * 15 

	titulo = "Resultados del examen: " + str(quiz.quiz)
	sheet.write_merge(2,2,0,2,titulo)


	x=5		

	sheet.write(x,0,'Nombre')
	sheet.write(x,1,'Calificacion')
	sheet.write(x,2,'Fecha')	
	x+=1

	
	for r in res:
	    sheet.write(x,0,r.nombre)
	    sheet.write(x,1,r.calif)
	    sheet.write(x,2,r.fecha,date_style)
	 
	    x+=1
            #sheet.write(row, col, val)
	

	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Resultados_'+str(quiz.quiz)+'.xls'
	book.save(response)
	return response

