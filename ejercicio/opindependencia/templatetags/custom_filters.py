from datetime import datetime,date
from axtel.headline.models import *
from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

today = date.today()

@register.filter
@stringfilter
def hoyhoy(value):
   print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 
   print value , " - ", today
   if value == str(today):
       print "Verdadero"
       return True
   else:
       print "FALSOOOO"
       return False
