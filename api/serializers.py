from re import L
from rest_framework import serializers
from stockin.models import (
  StockinBasic,
  StockinDetail,
  Barcode
)
from params.models import ItemInfo, Unit

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
            "code",
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