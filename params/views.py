from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Unit, Department, ItemType
from .forms import (
    UnitModelForm,
    DepartmentModelForm,
    ItemTypeCreateModelForm,
    ItemTypeUpdateModelForm,
)

# Unit view
class UnitListView(ListView):
    queryset = Unit.objects.all()
    template_name = 'unit/unit_list.html'

class UnitCreateView(CreateView):
    template_name = 'unit/unit_create.html'
    form_class = UnitModelForm
    queryset = Unit.objects.all()
    # success_url = reverse("unit:unit-list")

class UnitUpdateView(UpdateView):
    template_name = 'unit/unit_create.html'
    form_class = UnitModelForm
    queryset = Unit.objects.all()

class UnitDetailView(DetailView):
    queryset = Unit.objects.all()
    template_name = 'unit/unit_detail.html'

class UnitDeleteView(DeleteView):
    queryset = Unit.objects.all()
    template_name = 'unit/unit_delete.html'

    def get_success_url(self):
        return reverse('params:unit-list')

# Department view
class DepartmentListView(ListView):
    queryset = Department.objects.all()
    template_name = 'department/department_list.html'

class DepartmentCreateView(CreateView):
    template_name = 'department/department_create.html'
    form_class = DepartmentModelForm
    queryset = Department.objects.all()
    # success_url = reverse("department:department-list")

class DepartmentUpdateView(UpdateView):
    template_name = 'department/department_create.html'
    form_class = DepartmentModelForm
    queryset = Department.objects.all()

class DepartmentDetailView(DetailView):
    queryset = Department.objects.all()
    template_name = 'department/department_detail.html'

class DepartmentDeleteView(DeleteView):
    queryset = Department.objects.all()
    template_name = 'department/department_delete.html'

    def get_success_url(self):
        return reverse('params:department-list')

# ItemType
class ItemTypeCreateView(CreateView):
    template_name = 'itemtype/itemtype_create.html'
    form_class = ItemTypeCreateModelForm
    queryset = ItemType.objects.all()
    # success_url = reverse("unit:unit-list")

class ItemTypeListView(ListView):
    queryset = ItemType.objects.all()
    template_name = 'itemtype/itemtype_list.html'

class ItemTypeUpdateView(UpdateView):
    template_name = 'itemtype/itemtype_create.html'
    form_class = ItemTypeUpdateModelForm
    queryset = ItemType.objects.all()

class ItemTypeDetailView(DetailView):
    queryset = ItemType.objects.all()
    template_name = 'itemtype/itemtype_detail.html'

class ItemTypeDeleteView(DeleteView):
    queryset = ItemType.objects.all()
    template_name = 'itemtype/itemtype_delete.html'

    def get_success_url(self):
        return reverse('params:itemtype-list')
