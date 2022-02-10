from django.shortcuts import render
from django.views.generic import (
    ListView
)

from .models import Unit

class UnitListView(ListView):
    queryset = Unit.objects.all();
    template_name = 'unit/list.html'
