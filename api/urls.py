from django.urls import path
from .views import (
  StockinInfo,
  ItemsAll,
  stockin_save,
  StockinConfirm,
  StockinList,
  BarcodeList,
)

app_name = 'api'
urlpatterns = [
  path('stockin/<int:pk>/', StockinInfo.as_view()),
  path('allitems/', ItemsAll.as_view()),
  path('stockin/create/', stockin_save),
  path('stockin/confirm/<int:pk>/', StockinConfirm.as_view()),
  path('stockin/list/', StockinList.as_view()),
  path('barcodes/<int:detail>/', BarcodeList.as_view()),
]
