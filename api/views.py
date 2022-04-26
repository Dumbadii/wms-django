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
  StockinBasicListSerializer,
  StockinBasicSerializer,
  StockoutBasicSerializer,
  StockoutBasicListSerializer,
  StockoutBasicGetSerializer,
  StockbackBasicListSerializer,
  BarcodeSerializer,
  ItemInfoSerializer,
  ItemTypeSerializer,
  EmployeeSerializer,
  DepartmentSerializer
)
from stockin.models import (
  StockinBasic,
  StockoutBasic,
  StockbackBasic,
  Barcode,
)
from params.models import (
  ItemInfo,
  ItemType,
  Department,
)
from user.models import Employee

# Create your views here.

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

class StockinInfo(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        basic = StockinBasic.objects.get(pk=pk)
        serializer = StockinBasicGetSerializer(basic)
        return Response(serializer.data)

class StockoutInfo(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        basic = StockoutBasic.objects.get(pk=pk)
        serializer = StockoutBasicGetSerializer(basic)
        return Response(serializer.data)

class BarcodeList(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, detail):
        barcodes = Barcode.objects.filter(stockin_detail=detail)
        print(barcodes)
        serializer = BarcodeSerializer(barcodes, many=True)
        return Response(serializer.data)

class BarcodesIn(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        barcodes = Barcode.objects.filter(status=1)
        serializer = BarcodeSerializer(barcodes, many=True)
        return Response(serializer.data)

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
          detail.barcode.save()
        # serializer = StockoutBasicGetSerializer(basic)
        return Response('%s confirmed' %(basic.code))

class StockinList(generics.ListAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    pagination_class = PageNumberPagination
    queryset = StockinBasic.objects.all()
    serializer_class = StockinBasicListSerializer

class StockoutList(generics.ListAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    pagination_class = PageNumberPagination
    queryset = StockoutBasic.objects.all()
    serializer_class = StockoutBasicListSerializer

class StockbackList(generics.ListAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    pagination_class = PageNumberPagination
    queryset = StockbackBasic.objects.all()
    serializer_class = StockbackBasicListSerializer

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
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = ItemInfo.objects.all()
        serializer = ItemInfoSerializer(items, many=True)
        return Response(serializer.data)

class ItemsIn(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = ItemInfo.objects.all()
        serializer = ItemInfoSerializer(items, many=True)
        return Response(serializer.data)

class EmployeeList(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

class DepartmentList(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)