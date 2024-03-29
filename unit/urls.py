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
)

app_name = 'unit'
urlpatterns = [
    path('list/', UnitListView.as_view(), name='unit-list'),
    path('<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),
    path('<int:pk>/update/', UnitUpdateView.as_view(), name='unit-update'),
    path('<int:pk>/delete/', UnitDeleteView.as_view(), name='unit-delete'),
    path('create/', UnitCreateView.as_view(), name='unit-create'),
]
