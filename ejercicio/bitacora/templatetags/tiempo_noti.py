"""
from django import template

register = template.Library()

@register.filter
def convert(seg):
	tiempo = str(timedelta(seconds=seg)
	return "%s" % tiempo"""
from datetime import datetime, timedelta, time
from axtel.headline.models import *
from django import template
register = template.Library()

today = datetime.now()


@register.simple_tag
def foobarbaz(input):
    if "foo" == input:
        return "foo"
    if "bar" == input:
        return "bar"
    if "baz" == input:
        return "baz"
    return ""

@register.simple_tag
def convert(input):
    	return input

@register.simple_tag
def check(input):
	seg = int(input)
	if seg < 1800:
		return 'error'
	elif seg < 7200:
		return 'warning'
	else:
		return 'success'


@register.simple_tag
def saludo(input):
    	return str(input)


@register.simple_tag
def cliente(input):
	idcli = int(input)
	c = Clientes.objects.get(idcli=idcli)
	return c.cliente

@register.simple_tag
def idcli(input):
	idcli = int(input)
	c = Clientes.objects.get(idcli=idcli)
	return c.idcli



@property
def hoy(self):
   if self.date == '2012-01-09':
       return True
   else:
       return False
