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
	#a = timedelta(seconds=int(input))
	#return a
	seconds = int(input)
    	hours = seconds / 3600
    	seconds -= 3600*hours
    	minutes = seconds / 60
    	seconds -= 60*minutes
    	if hours == 0:
            return "%02d:%02d" % (minutes, seconds)
    	return "%02d:%02d:%02d" % (hours, minutes, seconds)

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
