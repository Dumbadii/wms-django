from re import L
from rest_framework import serializers
from stockin.models import (
  StockinBasic,
  StockinDetail,
  StockoutBasic,
  StockoutDetail,
  Barcode,
)
from params.models import (
    ItemInfo,
    Unit,
    ItemType,
    Department
)

from user.models import Employee
from django.contrib.auth.models import User

class DepartmentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Department
        fields = (
            "id",
            "code",
            "name",
        )

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )

class UnitSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Unit
        fields = (
            "name",
        )

class BarcodeSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Barcode
        fields = (
            "id",
            "code",
            "item",
            "amount",
        )

class ItemInfoSerializer(serializers.ModelSerializer):    
    unit = UnitSerializer()
    class Meta:
        model = ItemInfo
        fields = (
            "id",
            "code",
            "name",
            "brand",
            "type2",
            "specification",
            "unit"
        )

class StockinDetailGetSerializer(serializers.ModelSerializer):    
    item = ItemInfoSerializer() 
    class Meta:
        model = StockinDetail
        fields = (
            "id",
            "item",
            "barcode_count",
            "amount",
            "price"
        )

class StockinDetailSerializer(serializers.ModelSerializer):    
    id = serializers.IntegerField(required=False)
    class Meta:
        model = StockinDetail
        fields = (
            "id",
            "item",
            "barcode_count",
            "amount",
            "price"
        )

class StockinBasicSerializer(serializers.ModelSerializer):
    details = StockinDetailSerializer(many=True)

    class Meta:
        model = StockinBasic
        fields = (
            "id",
            "code",
            "vendor",
            "memo",
            "details",
        )
    
    def create(self, validated_data):
        details = validated_data.pop('details')
        basic = StockinBasic.objects.create(**validated_data)

        for detail in details:
            del detail['id']
            StockinDetail.objects.create(basic=basic, **detail)
            
        return basic

    def update(self, instance, validated_data):
        instance.memo = validated_data.get('memo', instance.memo)
        instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.save()
        details = validated_data.get('details')

        detail_ids = [item['id'] for item in details]
        for d in StockinDetail.objects.filter(basic=instance.id):
            if d.id not in detail_ids:
                d.delete()
        for detail in details:
            pk = detail['id']
            if(pk > 0):
                obj = StockinDetail.objects.get(id=pk)
                obj.price = detail['price']
                obj.amount = detail['amount']
                obj.barcode_count = detail['barcode_count']
                print(obj.price, obj.amount, obj.barcode_count)
                obj.save()
            else:
                obj = StockinDetail(
                    basic=instance,
                    item=detail['item'],
                    price=detail['price'],
                    amount=detail['amount'],
                    barcode_count=detail['barcode_count']
                )
                obj.save()
        return instance

class StockoutDetailSerializer(serializers.ModelSerializer):    
    id = serializers.IntegerField(required=False)
    class Meta:
        model = StockoutDetail
        fields = (
            "id",
            "barcode",
        )

class StockoutBasicSerializer(serializers.ModelSerializer):
    details = StockoutDetailSerializer(many=True)

    class Meta:
        model = StockoutBasic
        fields = (
            "id",
            "employee",
            "department",
            "operator",
            "memo",
            "details",
        )
    
    def create(self, validated_data):
        details = validated_data.pop('details')
        basic = StockoutBasic.objects.create(**validated_data)

        for detail in details:
            barcode = detail['barcode']
            if barcode.status.statusId == 1:
                obj = Barcode.objects.get(id=barcode.id)
                obj.status_id = 3
                obj.save()
                del detail['id']
                StockoutDetail.objects.create(basic=basic, **detail)
            
        return basic

    def update(self, instance, validated_data):
        instance.memo = validated_data.get('memo', instance.memo)
        instance.employee = validated_data.get('employee', instance.employee)
        instance.department = validated_data.get('department', instance.department)
        instance.save()
        details = validated_data.get('details')

        detail_ids = [item['id'] for item in details]
        for d in StockoutDetail.objects.filter(basic=instance.id):
            if d.id not in detail_ids:
                d.barcode.status_id = 1
                d.barcode.save()
                d.delete()
        for detail in details:
            pk = int(detail['id'])
            if(pk == 0):
                obj = StockoutDetail(
                    basic = instance,
                    barcode = detail['barcode']
                )
                obj.save()
                obj.barcode.statusId = 3
                obj.barcode.save()
        return instance

class StockoutDetailGetSerializer(serializers.ModelSerializer):
    barcode = BarcodeSerializer()    
    class Meta:
        model = StockoutDetail
        fields = (
            "id", 
            "barcode",
        )

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()    
    class Meta:
        model = Employee
        fields = (
            "id", 
            "user",
            "department"
        )

class StockoutBasicGetSerializer(serializers.ModelSerializer):
    details = StockoutDetailGetSerializer(many=True)
    # employee = EmployeeSerializer()

    class Meta:
        model = StockoutBasic
        fields = (
            "id",
            "code",
            "create_date",
            "employee",
            "department",
            "memo",
            "confirmed",
            "details",
        )

class StockinBasicGetSerializer(serializers.ModelSerializer):
    details = StockinDetailGetSerializer(many=True)

    class Meta:
        model = StockinBasic
        fields = (
            "id",
            "code",
            "create_date",
            "vendor",
            "memo",
            "confirmed",
            "details",
            "confirmed"
        )

class StockinBasicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockinBasic
        fields = (
            "id",
            "code",
            "create_date",
            "vendor",
            "memo",
            "confirmed",
        )

class StockoutBasicListSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'code': instance.code,
            'employee': instance.employee.user.username,
            'department': instance.department.name,
            'create_date': instance.create_date,
            'confirmed': instance.confirmed,
        }

class StockbackBasicListSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'code': instance.code,
            'employee': instance.employee.user.username,
            'department': instance.department.name,
            'create_date': instance.create_date,
            'confirmed': instance.confirmed,
        }

class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = (
            'id',
            'code',
            'name',
            'parent'
        )