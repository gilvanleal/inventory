from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, AllowAny, IsAuthenticatedOrReadOnly

from .models import Product, Movement, Partner, Location
from .serializers import ProductSerializer, MovementSerializer
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'])
    def movement(self, request, pk=None):
        import ipdb; ipdb.set_trace();
        movs = Movement.objects.filter(product=pk).order_by('-data')
        page = self.paginate_queryset(movs)
        if page is not None:
            serializer = MovementSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = MovementSerializer(movs, many=True, context={'request': request})
        return Response(serializer.data)


class MovementViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer


class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer