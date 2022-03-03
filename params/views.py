from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Unit, Department, ItemType, ItemInfo
from .forms import (
    UnitModelForm,
    DepartmentModelForm,
    ItemTypeCreateModelForm,
    ItemTypeUpdateModelForm,
    ItemInfoCreateModelForm,
    ItemInfoUpdateModelForm,
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

# ItemInfo
def load_types(request):
    type_id = request.GET.get('type')
    types = ItemType.objects.filter(parent=type_id)
    return render(request, 'itemtype/type_dropdown_list_options.html', {'types': types})

def load_items(request):
    type_id = request.GET.get('type')
    items = ItemInfo.objects.filter(type2=type_id)
    return render(request, 'iteminfo/item_dropdown_list_options.html', {'items': items})


class ItemInfoCreateView(CreateView):
    template_name = 'iteminfo/iteminfo_create.html'
    form_class = ItemInfoCreateModelForm
    queryset = ItemInfo.objects.all()
    # success_url = reverse("unit:unit-list")

class ItemInfoListView(ListView):
    queryset = ItemInfo.objects.all()
    template_name = 'iteminfo/iteminfo_list.html'

class ItemInfoUpdateView(UpdateView):
    template_name = 'iteminfo/iteminfo_create.html'
    form_class = ItemInfoUpdateModelForm
    queryset = ItemInfo.objects.all()

class ItemInfoDetailView(DetailView):
    queryset = ItemInfo.objects.all()
    template_name = 'iteminfo/iteminfo_detail.html'

class ItemInfoDeleteView(DeleteView):
    queryset = ItemInfo.objects.all()
    template_name = 'iteminfo/iteminfo_delete.html'

    def get_success_url(self):
        return reverse('params:iteminfo-list')
