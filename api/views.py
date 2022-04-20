from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.response import Response
from .serializers import (
  StockinBasicGetSerializer,
  StockinBasicListSerializer,
  StockinBasicSerializer,
  BarcodeSerializer,
  ItemInfoSerializer,
)
from stockin.models import (
  StockinBasic,
  Barcode,
)
from params.models import (
  ItemInfo,
)

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
  
class StockinInfo(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        basic = StockinBasic.objects.get(pk=pk)
        serializer = StockinBasicGetSerializer(basic)
        return Response(serializer.data)

class BarcodeList(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, detail):
        barcodes = Barcode.objects.filter(stockin_detail=detail)
        print(barcodes)
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

class ItemsAll(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = ItemInfo.objects.all()
        serializer = ItemInfoSerializer(items, many=True)
        return Response(serializer.data)

class StockinList(generics.ListAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    pagination_class = PageNumberPagination
    queryset = StockinBasic.objects.all()
    serializer_class = StockinBasicListSerializer
    # def get(self, request, format=None):
        # stockins = StockinBasic.objects.all()
        # serializer = StockinBasicListSerializer(stockins, many=True)
        # return Response(serializer.data)