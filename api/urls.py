from django.urls import path
from .views import (
  StockinInfo,
  StockoutInfo,
  ItemsAll,
  Type1List,
  Type2List,
  StockinConfirm,
  StockoutConfirm,
  StockinList,
  StockoutList,
  StockbackList,
  BarcodeList,
  EmployeeList,
  DepartmentList,
  BarcodesIn,
  stockin_save,
  stockout_save,
)

app_name = 'api'
urlpatterns = [
  path('stockin/<int:pk>/', StockinInfo.as_view()),
  path('stockout/<int:pk>/', StockoutInfo.as_view()),
  path('employees/', EmployeeList.as_view()),
  path('departments/', DepartmentList.as_view()),
  path('items/', ItemsAll.as_view()),
  path('type1/', Type1List.as_view()),
  path('type2/', Type2List.as_view()),
  path('stockin/create/', stockin_save),
  path('stockout/create/', stockout_save),
  path('stockin/confirm/<int:pk>/', StockinConfirm.as_view()),
  path('stockout/confirm/<int:pk>/', StockoutConfirm.as_view()),
  path('stockin/list/', StockinList.as_view()),
  path('stockout/list/', StockoutList.as_view()),
  path('stockback/list/', StockbackList.as_view()),
  path('barcodes/<int:detail>/', BarcodeList.as_view()),
  path('barcodes/in/', BarcodesIn.as_view()),
]
