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
)

app_name = 'stockin'
urlpatterns = [
    # path('iteminfo/list/', ItemInfoListView.as_view(), name='iteminfo-list'),
    # path('iteminfo/<int:pk>/', ItemInfoDetailView.as_view(), name='iteminfo-detail'),
    # path('iteminfo/<int:pk>/update/', ItemInfoUpdateView.as_view(), name='iteminfo-update'),
    # path('iteminfo/<int:pk>/delete/', ItemInfoDeleteView.as_view(), name='iteminfo-delete'),
    path('create/', StockinCreateView.as_view(), name='stockin-create'),
    # path('iteminfo/ajax/load-types/', load_types, name='iteminfo-ajax_load_types')
]
