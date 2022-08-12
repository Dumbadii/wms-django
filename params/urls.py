"""wms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import (
    UnitListView,
    UnitCreateView,
    UnitDetailView,
    UnitUpdateView,
    UnitDeleteView,
    DepartmentListView,
    DepartmentCreateView,
    DepartmentDetailView,
    DepartmentUpdateView,
    DepartmentDeleteView,
    ItemTypeCreateView,
    ItemTypeDetailView,
    ItemTypeUpdateView,
    ItemTypeDeleteView,
    ItemTypeListView,
    ItemInfoCreateView,
    ItemInfoDetailView,
    ItemInfoUpdateView,
    ItemInfoDeleteView,
    ItemInfoListView,
    load_types,
    load_items,
)

app_name = 'params'
urlpatterns = [
    path('unit/list/', UnitListView.as_view(), name='unit-list'),
    path('unit/<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),
    path('unit/<int:pk>/update/', UnitUpdateView.as_view(), name='unit-update'),
    path('unit/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit-delete'),
    path('unit/create/', UnitCreateView.as_view(), name='unit-create'),

    path('department/list/', DepartmentListView.as_view(), name='department-list'),
    path('department/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('department/<int:pk>/update/', DepartmentUpdateView.as_view(), name='department-update'),
    path('department/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department-delete'),
    path('department/create/', DepartmentCreateView.as_view(), name='department-create'),

    path('itemtype/list/', ItemTypeListView.as_view(), name='itemtype-list'),
    path('itemtype/<int:pk>/', ItemTypeDetailView.as_view(), name='itemtype-detail'),
    path('itemtype/<int:pk>/update/', ItemTypeUpdateView.as_view(), name='itemtype-update'),
    path('itemtype/<int:pk>/delete/', ItemTypeDeleteView.as_view(), name='itemtype-delete'),
    path('itemtype/create/', ItemTypeCreateView.as_view(), name='itemtype-create'),
    path('itemtype/ajax/load-types/', load_types, name='ajax_load_types'),

    path('iteminfo/list/', ItemInfoListView.as_view(), name='iteminfo-list'),
    path('iteminfo/<int:pk>/', ItemInfoDetailView.as_view(), name='iteminfo-detail'),
    path('iteminfo/<int:pk>/update/', ItemInfoUpdateView.as_view(), name='iteminfo-update'),
    path('iteminfo/<int:pk>/delete/', ItemInfoDeleteView.as_view(), name='iteminfo-delete'),
    path('iteminfo/create/', ItemInfoCreateView.as_view(), name='iteminfo-create'),
    path('iteminfo/ajax/load-itmes/', load_items, name='ajax_load_items')
]
