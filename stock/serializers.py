from rest_framework import routers, serializers, viewsets
from .models import Product, Movement, Partner, Location

# Serializers define the API representation.


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    quantity = serializers.IntegerField(min_value=0, read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'sku', 'price', 'quantity')


class MovementSerializer(serializers.HyperlinkedModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        if data['kind'] == Movement.OUT:
            if data['quantity'] > data['product'].quantity:
                raise serializers.ValidationError('Stock out')
            if data.get('partner', False) and not data['partner'].client:
                raise serializers.ValidationError('This partner is not a client')
        if data['kind'] == Movement.IN:
            if data.get('partner', False) and not data['partner'].supplier:
                raise serializers.ValidationError('This partner is not a supplier')
        return data

    class Meta:
        model = Movement
        fields = ('kind', 'partner', 'location', 'data', 'product', 'quantity')


class PartnerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Partner
        fields = ('name', 'cp', 'client', 'supplier')


class LocationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Location
        fields = ('name', 'kind')
