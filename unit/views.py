from django.urls import reverse
from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Unit, Department
from .forms import UnitModelForm, DepartmentModelForm

# Unit view
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

# Department view
class DepartmentListView(ListView):
    queryset = Department.objects.all()
    template_name = 'department_list.html'

class DepartmentCreateView(CreateView):
    template_name = 'department_create.html'
    form_class = DepartmentModelForm
    queryset = Department.objects.all()
    # success_url = reverse("department:department-list")

class DepartmentUpdateView(UpdateView):
    template_name = 'department_create.html'
    form_class = DepartmentModelForm
    queryset = Department.objects.all()

class DepartmentDetailView(DetailView):
    queryset = Department.objects.all()
    template_name = 'department_detail.html'

class DepartmentDeleteView(DeleteView):
    queryset = Department.objects.all()
    template_name = 'department_delete.html'

    def get_success_url(self):
        return reverse('department:department-list')