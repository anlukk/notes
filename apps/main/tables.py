import django_tables2 as tables
from .models import SimpleNote


class MyNote_Table(tables.Table):

    class Meta:
        model = SimpleNote
        attrs = {"class": "table"}