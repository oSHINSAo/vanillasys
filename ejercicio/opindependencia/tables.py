import django_tables2 as tables
from ejercicio.opindependencia.models import *

class AttackTable(tables.Table):
    class Meta:
        model = ClientesAttack
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
	fields = ('idcla', 'idcli', 'tipo','consecuencia','idsta')
