from django.urls import reverse
from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Unit
from .forms import UnitModelForm

class UnitListView(ListView):
    queryset = Unit.objects.all()
    template_name = 'unit_list.html'

class UnitCreateView(CreateView):
    template_name = 'unit_create.html'
    form_class = UnitModelForm
    queryset = Unit.objects.all()
    # success_url = reverse("unit:unit-list")

class UnitUpdateView(UpdateView):
    template_name = 'unit_create.html'
    form_class = UnitModelForm
    queryset = Unit.objects.all()

class UnitDetailView(DetailView):
    queryset = Unit.objects.all()
    template_name = 'unit_detail.html'

class UnitDeleteView(DeleteView):
    queryset = Unit.objects.all()
    template_name = 'unit_delete.html'

    def get_success_url(self):
        return reverse('unit:unit-list')