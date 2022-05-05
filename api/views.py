from re import I
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from .serializers import (
  StockinBasicGetSerializer,
  StockoutBasicGetSerializer,
  StockbackBasicGetSerializer,
  StockinBasicListSerializer,
  StockinBasicSerializer,
  StockoutBasicSerializer,
  StockoutBasicListSerializer,
  StockbackBasicSerializer,
  StockbackBasicListSerializer,
  StockdisableBasicSerializer,
  StockdisableBasicListSerializer,
  StockdisableBasicGetSerializer,
  BarcodeSerializer,
  BarcodeDetailSerializer,
  ItemInfoSerializer,
  ItemTypeSerializer,
  EmployeeSerializer,
  DepartmentSerializer,
  BarcodeStatusSerializer,
)
from stockin.models import (
  StockinBasic,
  StockoutBasic,
  StockbackBasic,
  StockdisableBasic,
  Barcode,
)
from params.models import (
  ItemInfo,
  ItemType,
  Department,
  BarcodeStatus,
)
from user.models import Employee

# Create your views here.
class BarcodesByDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, detail):
        barcodes = Barcode.objects.filter(stockin_detail=detail)
        print(barcodes)
        serializer = BarcodeSerializer(barcodes, many=True)
        return Response(serializer.data)

class BarcodesByStatus(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, statusId):
        print('statusId:',statusId)
        barcodes = Barcode.objects.filter(status=statusId)
        serializer = BarcodeSerializer(barcodes, many=True)
        return Response(serializer.data)

class Type1List(APIView):
    def get(self, request):
        types = ItemType.objects.filter(parent__isnull=True)
        serializer = ItemTypeSerializer(types, many=True)
        return Response(serializer.data)

class Type2List(APIView):
    def get(self, request):
        types = ItemType.objects.filter(parent__isnull=False)
        serializer = ItemTypeSerializer(types, many=True)
        return Response(serializer.data)

class ItemsAll(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = ItemInfo.objects.all()
        serializer = ItemInfoSerializer(items, many=True)
        return Response(serializer.data)

class ItemsIn(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = ItemInfo.objects.all()
        serializer = ItemInfoSerializer(items, many=True)
        return Response(serializer.data)

class EmployeeList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

class DepartmentList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

class StatusList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        status = BarcodeStatus.objects.all()
        serializer = BarcodeStatusSerializer(status, many=True)
        return Response(serializer.data)

# stockin----------------------------------
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def stockin_save(request):
  pk = int(request.data['id'])
  print(request.data)
  if pk > 0:
    obj = StockinBasic.objects.get(id=pk)
    serializer = StockinBasicSerializer(obj,data=request.data)
  else:
    serializer = StockinBasicSerializer(data=request.data)

  if serializer.is_valid():
    try:
        serializer.save(operator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class StockinConfirm(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        basic = StockinBasic.objects.get(id=pk)
        basic.confirmed = True
        basic.save()
        print('%s confirmed' %(pk))
        for detail in basic.details.all():
          detail.gen_barcode()
        # serializer = StockinBasicGetSerializer(basic)
        return Response('%s confirmed' %(basic.code))

class StockinInfo(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        basic = StockinBasic.objects.get(pk=pk)
        serializer = StockinBasicGetSerializer(basic)
        return Response(serializer.data)

class StockinList(generics.ListAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    pagination_class = PageNumberPagination
    queryset = StockinBasic.objects.order_by('-create_date')
    serializer_class = StockinBasicListSerializer

# stockout--------------------------------------------------
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def stockout_save(request):
  pk = int(request.data['id'])
  if pk > 0:
    obj = StockoutBasic.objects.get(id=pk)
    serializer = StockoutBasicSerializer(obj,data=request.data)
  else:
    serializer = StockoutBasicSerializer(data=request.data)
  print(request.data)
  if serializer.is_valid():
    try:
        serializer.save(operator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
  print(serializer.errors)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockoutInfo(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        basic = StockoutBasic.objects.get(pk=pk)
        serializer = StockoutBasicGetSerializer(basic)
        return Response(serializer.data)

class StockoutConfirm(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        basic = StockoutBasic.objects.get(id=pk)
        basic.confirmed = True
        basic.save()
        print('%s confirmed' %(pk))
        for detail in basic.details.all():
          print(detail.barcode, detail.barcode.status)
          detail.barcode.status_id = 2
          detail.barcode.department = basic.department
          detail.barcode.save()
        # serializer = StockoutBasicGetSerializer(basic)
        return Response('%s confirmed' %(basic.code))

class StockoutList(generics.ListAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    pagination_class = PageNumberPagination
    queryset = StockoutBasic.objects.order_by('-create_date')
    serializer_class = StockoutBasicListSerializer

# stockback-------------------------------------------
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def stockback_save(request):
  pk = int(request.data['id'])
  if pk > 0:
    obj = StockbackBasic.objects.get(id=pk)
    serializer = StockbackBasicSerializer(obj,data=request.data)
  else:
    serializer = StockbackBasicSerializer(data=request.data)
  print(request.data)
  if serializer.is_valid():
    try:
        serializer.save(operator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
  print('not validate')
  print(serializer.errors)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockbackInfo(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        basic = StockbackBasic.objects.get(pk=pk)
        serializer = StockbackBasicGetSerializer(basic)
        return Response(serializer.data)

class StockbackConfirm(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        basic = StockbackBasic.objects.get(id=pk)
        basic.confirmed = True
        basic.save()
        print('%s confirmed' %(pk))
        for detail in basic.details.all():
          print(detail.barcode, detail.barcode.status)
          detail.barcode.status_id = 1
          detail.barcode.save()
        # serializer = StockbackBasicGetSerializer(basic)
        return Response('%s confirmed' %(basic.code))


class StockbackList(generics.ListAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    pagination_class = PageNumberPagination
    queryset = StockbackBasic.objects.order_by('-create_date')
    serializer_class = StockbackBasicListSerializer

# stockdisable----------------------------------
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def stockdisable_save(request):
  pk = int(request.data['id'])
  if pk > 0:
    obj = StockdisableBasic.objects.get(id=pk)
    serializer = StockdisableBasicSerializer(obj,data=request.data)
  else:
    serializer = StockdisableBasicSerializer(data=request.data)
  print(request.data)
  if serializer.is_valid():
    try:
        serializer.save(operator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
  print('not validate')
  print(serializer.errors)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockdisableInfo(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        basic = StockdisableBasic.objects.get(pk=pk)
        serializer = StockdisableBasicGetSerializer(basic)
        return Response(serializer.data)

class StockdisableConfirm(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        basic = StockdisableBasic.objects.get(id=pk)
        basic.confirmed = True
        basic.save()
        print('%s confirmed' %(pk))
        for detail in basic.details.all():
          print(detail.barcode, detail.barcode.status)
          detail.barcode.status_id = 4
          detail.barcode.save()
        # serializer = StockdisableBasicGetSerializer(basic)
        return Response('%s confirmed' %(basic.code))


class StockdisableList(generics.ListAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    pagination_class = PageNumberPagination
    queryset = StockdisableBasic.objects.order_by('-create_date')
    serializer_class = StockdisableBasicListSerializer

# search filter-------------------
class BarcodeSearch(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    pagination_class = PageNumberPagination
    queryset = Barcode.objects.all()
    serializer_class = BarcodeDetailSerializer

    def get_queryset(self):
        queryset = self.queryset
        itemName = self.request.query_params.get('itemName', None)
        type1 = self.request.query_params.get('type1', None)
        type2 = self.request.query_params.get('type2', None)
        item = self.request.query_params.get('item', None)
        item = self.request.query_params.get('item', None)
        status = self.request.query_params.get('status', None)
        department = self.request.query_params.get('department', None)
        code = self.request.query_params.get('code', None)

        print('t1%s-t2%s-st%s-item%s' %(type1, type2, status, item))
        print(self.request.query_params)

        if itemName is not None:
            queryset = queryset.filter(item__name__contains=itemName)
        if item is not None:
            queryset = queryset.filter(item__code=item)
        if type1 is not None:
            queryset = queryset.filter(item__type1__code=type1)
        if type2 is not None:
            queryset = queryset.filter(item__type2__code=type2)
        if status is not None:
            queryset = queryset.filter(status__statusId=status)
        if department is not None:
            queryset = queryset.filter(department=department)
        if code is not None:
            queryset = queryset.filter(code__contains=code)
        

        return queryset

class InventoryStat(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
      total = Barcode.objects.count()
      inCnt = Barcode.objects.filter(~Q(status__statusId=4) & Q(department=1)).count()
      outCnt = Barcode.objects.filter(~Q(status__statusId=4) & ~Q(department=1)).count()
      disableCnt = Barcode.objects.filter(status__statusId=4).count()

      deptStat =[{'name':obj.name, 'cnt':obj.barcodes.count()} for obj in Department.objects.all()]
      
      result = {
        'total': total,
        'inCnt': inCnt,
        'outCnt': outCnt,
        'disableCnt': disableCnt,
        'deptStat': deptStat
      }
      print(result)
      return Response(result)