from re import L
from unittest import mock
from rest_framework import serializers
from stockin.models import (
  StockinBasic,
  StockinDetail,
  StockoutBasic,
  StockbackBasic,
  StockoutDetail,
  StockbackDetail,
  StockdisableBasic,
  StockdisableDetail,
  Barcode,
)
from params.models import (
    BarcodeStatus,
    ItemInfo,
    Unit,
    ItemTypeChild,
    ItemTypeParent,
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

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()    
    class Meta:
        model = Employee
        fields = (
            "id", 
            "user",
            "department"
        )

class UnitSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Unit
        fields = (
            "name",
        )

class BarcodeStatusSerializer(serializers.ModelSerializer):    
    class Meta:
        model = BarcodeStatus
        fields = (
            "statusId",
            "statusName",
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

class BarcodeDetailSerializer(serializers.BaseSerializer):    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'code': instance.code,
            'type1': instance.item.type2.parent.name,
            'type2': instance.item.type2.name,
            'item': instance.item.name,
            'unit': instance.item.unit.name,
            'department': instance.department.name,
            'amount': instance.amount,
            'status': instance.status.statusName
        }

class ItemTypeChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTypeChild
        fields = (
            'id',
            'code',
            'name',
            'parent'
        )

class ItemTypeParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTypeParent
        fields = (
            'id',
            'code',
            'name'
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
# stockin-----------------------------------
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
            # "code",
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

# stockout-----------------------------------------
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

class StockoutDetailGetSerializer(serializers.ModelSerializer):
    barcode = BarcodeSerializer()    
    class Meta:
        model = StockoutDetail
        fields = (
            "id", 
            "barcode",
        )

class StockoutDetailSerializer(serializers.ModelSerializer):    
    id = serializers.IntegerField(required=False)
    class Meta:
        model = StockoutDetail
        fields = (
            "id",
            "barcode",
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

# stockback-----------------------------------------------
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


class StockbackDetailGetSerializer(serializers.ModelSerializer):
    barcode = BarcodeSerializer()
    class Meta:
        model = StockbackDetail
        fields = (
            "id",
            "barcode"
        )

class StockbackBasicGetSerializer(serializers.ModelSerializer):
    details = StockbackDetailGetSerializer(many=True)
    # employee = EmployeeSerializer()

    class Meta:
        model = StockbackBasic
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

class StockbackDetailSerializer(serializers.ModelSerializer):    
    id = serializers.IntegerField(required=False)
    class Meta:
        model = StockbackDetail
        fields = (
            "id",
            "barcode",
        )

class StockbackBasicSerializer(serializers.ModelSerializer):
    details = StockbackDetailSerializer(many=True)

    class Meta:
        model = StockbackBasic
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
        basic = StockbackBasic.objects.create(**validated_data)

        for detail in details:
            barcode = detail['barcode']
            if barcode.status.statusId == 2:
                obj = Barcode.objects.get(id=barcode.id)
                obj.status_id = 3
                obj.save()
                del detail['id']
                StockbackDetail.objects.create(basic=basic, **detail)
            
        return basic

    def update(self, instance, validated_data):
        instance.memo = validated_data.get('memo', instance.memo)
        instance.employee = validated_data.get('employee', instance.employee)
        instance.department = validated_data.get('department', instance.department)
        instance.save()
        details = validated_data.get('details')

        detail_ids = [item['id'] for item in details]
        for d in StockbackDetail.objects.filter(basic=instance.id):
            if d.id not in detail_ids:
                d.barcode.status_id = 1
                d.barcode.save()
                d.delete()
        for detail in details:
            pk = int(detail['id'])
            if(pk == 0):
                obj = StockbackDetail(
                    basic = instance,
                    barcode = detail['barcode']
                )
                obj.save()
                obj.barcode.statusId = 3
                obj.barcode.save()
        return instance

# stockdisable-----------------------------------------------
class StockdisableBasicListSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'code': instance.code,
            'create_date': instance.create_date,
            'confirmed': instance.confirmed,
        }


class StockdisableDetailGetSerializer(serializers.ModelSerializer):
    barcode = BarcodeSerializer()
    class Meta:
        model = StockdisableDetail
        fields = (
            "id",
            "barcode"
        )

class StockdisableBasicGetSerializer(serializers.ModelSerializer):
    details = StockdisableDetailGetSerializer(many=True)

    class Meta:
        model = StockdisableBasic
        fields = (
            "id",
            "code",
            "create_date",
            "memo",
            "confirmed",
            "details",
        )

class StockdisableDetailSerializer(serializers.ModelSerializer):    
    id = serializers.IntegerField(required=False)
    class Meta:
        model = StockdisableDetail
        fields = (
            "id",
            "barcode",
        )

class StockdisableBasicSerializer(serializers.ModelSerializer):
    details = StockdisableDetailSerializer(many=True)

    class Meta:
        model = StockdisableBasic
        fields = (
            "id",
            "operator",
            "memo",
            "details",
        )
    
    def create(self, validated_data):
        details = validated_data.pop('details')
        basic = StockdisableBasic.objects.create(**validated_data)

        for detail in details:
            barcode = detail['barcode']
            if barcode.status.statusId == 1:
                obj = Barcode.objects.get(id=barcode.id)
                obj.status_id = 3
                obj.save()
                del detail['id']
                StockdisableDetail.objects.create(basic=basic, **detail)
            
        return basic

    def update(self, instance, validated_data):
        instance.memo = validated_data.get('memo', instance.memo)
        instance.save()
        details = validated_data.get('details')

        detail_ids = [item['id'] for item in details]
        for d in StockdisableDetail.objects.filter(basic=instance.id):
            if d.id not in detail_ids:
                d.barcode.status_id = 1
                d.barcode.save()
                d.delete()
        for detail in details:
            pk = int(detail['id'])
            if(pk == 0):
                obj = StockdisableDetail(
                    basic = instance,
                    barcode = detail['barcode']
                )
                obj.save()
                obj.barcode.statusId = 3
                obj.barcode.save()
        return instance
