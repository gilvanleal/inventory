from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, AllowAny, IsAuthenticatedOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Movement, Partner, Location
from .serializers import ProductSerializer, MovementSerializer, PartnerSerializer, LocationSerializer
# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'sku']
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    def movement(self, request, pk=None):
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product', 'data']
    ordering = ['-data']



class PartnerViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer



class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
