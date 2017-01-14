from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .models import Delivery, DeliveryVariant
from .models import DeliveryItem
from .models import CropForm
from .models import Culture
from .models import Crop

from .models import Customer
import simplejson
from collections import namedtuple
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from datetime import datetime

class Option:
    def __init__(self,id,name):
        self.id=id
        self.name=name
    def __str__(self):
        return self.name




class deliveries_harvest_for_delivery(View):
    def post(self,request):
        delivery_item_id = request.POST['id']
        delivery_item    = get_object_or_404 ( DeliveryItem, pk=delivery_item_id )

        data={'harvested_amount': delivery_item.harvested_amount(),
              'unit': delivery_item.order_unit_text(),
              'box_value':delivery_item.box_value(),


              'status':delivery_item.status(),
              'harvest_relation':delivery_item.harvest_relation(),
              'target_amount':delivery_item.total_order_amount(),
              'crop':delivery_item.cropform.crop.crop}
        return HttpResponse ( simplejson.dumps ( data ) )

class delivery_item_edit_price(View):
    def post(self,request):
        delivery_item = get_object_or_404(DeliveryItem, pk=request.POST['pk'])
        price = int(request.POST['value[amount]'])
        delivery_item.price = price

        if 'value[unit]' in request.POST:
            unit = request.POST['value[unit]']
            delivery_item.price_type = unit


        delivery_item.save()
        return HttpResponse ( "" )

class delivery_item_edit_amount(View):
    def post(self,request):
        delivery_item = get_object_or_404(DeliveryItem, pk=request.POST['pk'])
        price = float(request.POST['value[amount]'])
        delivery_item.price = price

        if 'value[unit]' in request.POST:
            unit = request.POST['value[unit]']
            delivery_item.amount_unit = unit


        delivery_item.save()
        return HttpResponse ( "" )

class values_for_deliveryitem(View):
    def post(self,request):
        delivery_item = get_object_or_404 ( DeliveryItem, pk=request.POST['pk'] )
        data={'pk':request.POST['pk'],
              'box_value':delivery_item.box_value(),
              'total_order_amount':delivery_item.total_order_amount(),
              'ordered_value':delivery_item.ordered_value(),
              'harvested_value':delivery_item.harvested_value(),
              'unit':delivery_item.order_unit_text(),
              'sum_ordered_value':delivery_item.delivery.total_order_value(),
              'sum_box_values_and_counts':delivery_item.delivery.box_values_and_counts(),
              'sum_harvested_value':delivery_item.delivery.total_harvested_value(),
              'box_num':delivery_item.delivery.variant_count()
              }
        return HttpResponse ( simplejson.dumps ( data ) )

class delivery_edit_target_date(View):
    def post(self,request):
        delivery = get_object_or_404(Delivery, pk=request.POST['pk'])
        d = datetime.strptime(request.POST['value'], '%Y-%m-%d')
        delivery.target_date=d
        delivery.save()
        return HttpResponse ("")

class delivery_variant_edit_count(View):
    def post(self,request):
        variant = get_object_or_404(DeliveryVariant, pk=request.POST['pk'])
        count = request.POST['value']
        variant.count=count
        variant.save()
        return HttpResponse ("")


class delivery_variant_included(View):
    def post(self,request):
        v_pk,di_pk = request.POST['pk'].split(',')
        variant = get_object_or_404(DeliveryVariant,pk=v_pk)
        delivery_item =  get_object_or_404(DeliveryItem,pk=di_pk)

        if 'value[]' in request.POST:
            variant.extempt.remove(delivery_item)
        else:
            variant.extempt.add(delivery_item)


        return HttpResponse ("")


