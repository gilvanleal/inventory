from rest_framework import routers, serializers, viewsets
from .models import Product, Movement

# Serializers define the API representation.


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    quantity = serializers.IntegerField(min_value=0, read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'sku', 'price', 'quantity')


class MovementSerializer(serializers.HyperlinkedModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        # import ipdb; ipdb.set_trace()
        if data['kind'] == Movement.OUT and data['quantity'] > data['product'].quantity:
            raise serializers.ValidationError('Stock out')
        return data

    class Meta:
        model = Movement
        fields = ('kind', 'partner', 'location', 'data', 'product', 'quantity')
