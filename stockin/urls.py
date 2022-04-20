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
    StockinConfirmView,
    StockinListView,
    StockinPdfView,
    StockoutCreateView,
    StockoutDetailView,
    StockoutDetailUpdateView,
    StockoutDeleteView,
    StockoutListView,
    StockoutConfirmView,
    StockoutPdfView,
    StockbackCreateView,
    StockbackDetailView,
    StockbackDetailUpdateView,
    StockbackDeleteView,
    StockbackListView,
    StockbackConfirmView,
    StockbackPdfView,
    StockinFilterListView,
)

app_name = 'stock'
urlpatterns = [
    path('in/', StockinListView.as_view(), name='stockin-home'),
    path('in/list/', StockinListView.as_view(), name='stockin-list'),
    path('in/list_f/', StockinFilterListView.as_view(), name='stockin-list_f'),
    path('in/create/', StockinCreateView.as_view(), name='stockin-create'),
    path('in/update/<int:pk>/', StockinDetailUpdateView.as_view(), name='stockin-update'),
    path('in/delete/<int:pk>/', StockinDeleteView.as_view(), name='stockin-delete'),
    path('in/<int:pk>/', StockinDetailView.as_view(), name='stockin-info'),
    path('in/confirm/<int:pk>/', StockinConfirmView.as_view(), name='stockin-confirm'),
    path('in/pdf/<int:pk>/', StockinPdfView.as_view(), name='stockin-pdf'),
    path('out/', StockoutListView.as_view(), name='stockout-home'),
    path('out/list/', StockoutListView.as_view(), name='stockout-list'),
    path('out/create/', StockoutCreateView.as_view(), name='stockout-create'),
    path('out/update/<int:pk>/', StockoutDetailUpdateView.as_view(), name='stockout-update'),
    path('out/delete/<int:pk>/', StockoutDeleteView.as_view(), name='stockout-delete'),
    path('out/<int:pk>/', StockoutDetailView.as_view(), name='stockout-info'),
    path('out/confirm/<int:pk>/', StockoutConfirmView.as_view(), name='stockout-confirm'),
    path('out/pdf/<int:pk>/', StockoutPdfView.as_view(), name='stockout-pdf'),
    path('back/', StockbackListView.as_view(), name='stockback-home'),
    path('back/list/', StockbackListView.as_view(), name='stockback-list'),
    path('back/create/', StockbackCreateView.as_view(), name='stockback-create'),
    path('back/update/<int:pk>/', StockbackDetailUpdateView.as_view(), name='stockback-update'),
    path('back/delete/<int:pk>/', StockbackDeleteView.as_view(), name='stockback-delete'),
    path('back/<int:pk>/', StockbackDetailView.as_view(), name='stockback-info'),
    path('back/confirm/<int:pk>/', StockbackConfirmView.as_view(), name='stockback-confirm'),
    path('back/pdf/<int:pk>/', StockbackPdfView.as_view(), name='stockback-pdf'),
]
