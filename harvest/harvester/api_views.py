from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DeliveryItemSerializer, DeliveryVariantSerializer, CustomerSerializer

from .models import DeliveryItem, DeliveryVariant, Customer


@api_view(['GET','PATCH'])
def delivery_item_element(request, pk):
    try:
        di = DeliveryItem.objects.get(pk=pk)
    except DeliveryItem.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PATCH':
        serializer = DeliveryItemSerializer ( di, data=request.data, partial=True )
        if serializer.is_valid ( ):
            serializer.save ( )
            di2 = DeliveryItem.objects.get ( pk=pk )
            serializer_out = DeliveryItemSerializer ( di2 )
            return Response ( serializer_out.data )



        return Response ( serializer.errors, status=status.HTTP_400_BAD_REQUEST )

    if request.method == 'GET':
        serializer = DeliveryItemSerializer(di)
        return Response(serializer.data)

@api_view(['GET','PATCH'])
def delivery_variant_element(request,pk):
    try:
        dv = DeliveryVariant.objects.get ( pk=pk )
    except DeliveryItem.DoesNotExist:
        return HttpResponse ( status=404 )

    if request.method == 'PATCH':
        serializer = DeliveryVariantSerializer(dv,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()

            dv2=DeliveryVariant.objects.get(pk=pk)
            serializer_out = DeliveryVariantSerializer(dv2)
            return Response(serializer_out.data)
    if request.method == 'GET':
        serializer = DeliveryVariantSerializer(dv)
        return Response(serializer.data)

@api_view(['PATCH'])
def customer_element(request,pk):
    c = get_object_or_404(Customer,pk=pk)
    if request.method == 'PATCH':
        serializer = CustomerSerializer(c,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response ( serializer.errors, status=status.HTTP_400_BAD_REQUEST )