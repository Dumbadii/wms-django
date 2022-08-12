from django.urls import path
from .views import (
  stockin_save,
  StockinInfo,
  StockinConfirm,
  StockinList,
  stockout_save,
  StockoutInfo,
  StockoutConfirm,
  StockoutList,
  stockback_save,
  StockbackInfo,
  StockbackConfirm,
  StockbackList,
  stockdisable_save,
  StockdisableInfo,
  StockdisableConfirm,
  StockdisableList,
  ItemsAll,
  Type1List,
  Type2List,
  StatusList,
  EmployeeList,
  DepartmentList,
  BarcodesByStatus,
  BarcodesByDetail,
  BarcodeSearch,
  InventoryStat,
  stockin_pdf,
  stockout_pdf,
  stockback_pdf,
  stockdisable_pdf,
  ItemTypeSave,
)

app_name = 'api'
urlpatterns = [
  path('stockin/<int:pk>/', StockinInfo.as_view()),
  path('stockin/create/', stockin_save),
  path('stockin/confirm/<int:pk>/', StockinConfirm.as_view()),
  path('stockin/list/', StockinList.as_view()),
  path('stockin/pdf/<int:pk>/', stockin_pdf),
  path('stockout/<int:pk>/', StockoutInfo.as_view()),
  path('stockout/create/', stockout_save),
  path('stockout/confirm/<int:pk>/', StockoutConfirm.as_view()),
  path('stockout/list/', StockoutList.as_view()),
  path('stockout/pdf/<int:pk>/', stockout_pdf),
  path('stockback/<int:pk>/', StockbackInfo.as_view()),
  path('stockback/create/', stockback_save),
  path('stockback/confirm/<int:pk>/', StockbackConfirm.as_view()),
  path('stockback/list/', StockbackList.as_view()),
  path('stockback/pdf/<int:pk>/', stockback_pdf),
  path('stockdisable/<int:pk>/', StockdisableInfo.as_view()),
  path('stockdisable/create/', stockdisable_save),
  path('stockdisable/confirm/<int:pk>/', StockdisableConfirm.as_view()),
  path('stockdisable/list/', StockdisableList.as_view()),
  path('stockdisable/pdf/<int:pk>/', stockdisable_pdf),
  path('employees/', EmployeeList.as_view()),
  path('departments/', DepartmentList.as_view()),
  path('items/', ItemsAll.as_view()),
  path('type1/', Type1List.as_view()),
  path('type2/', Type2List.as_view()),
  path('type_save/', ItemTypeSave.as_view()),
  path('status/', StatusList.as_view()),
  path('stat/', InventoryStat.as_view()),
  path('barcodes/detail/<int:detail>/', BarcodesByDetail.as_view()),
  path('barcodes/status/<int:statusId>/', BarcodesByStatus.as_view()),
  path('barcodes/search/', BarcodeSearch.as_view()),
]
