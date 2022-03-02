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
    StockinCreateView,
    StockinDetailView,
    StockinDetailUpdateView,
    StockinDeleteView,
    StockinListView,
)

app_name = 'stockin'
urlpatterns = [
    path('', StockinListView.as_view(), name='stockin-home'),
    path('list/', StockinListView.as_view(), name='stockin-list'),
    path('create/', StockinCreateView.as_view(), name='stockin-create'),
    path('update/<int:pk>/', StockinDetailUpdateView.as_view(), name='stockin-update'),
    path('delete/<int:pk>/', StockinDeleteView.as_view(), name='stockin-delete'),
    path('<int:pk>/', StockinDetailView.as_view(), name='stockin-info'),
]
