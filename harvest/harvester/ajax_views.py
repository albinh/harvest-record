from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import RedirectView

from .models import Delivery, DeliveryVariant, PriceItem, CustomerCategory
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


def values_for_delivery(request):
    delivery_item = get_object_or_404 ( DeliveryItem, pk=request.POST['pk'] )

    variants = [{'pk':v.pk, 'count':v.crop_count(), 'value':v.value()} for v in delivery_item.delivery.deliveryvariant_set.all()]

    data = {'pk': request.POST['pk'],
            'is_price_as_listed': delivery_item.is_price_as_listed ( ),
            'box_value': delivery_item.box_value ( ),
            'price':delivery_item.price,
            'price_unit':delivery_item.price_type,
            'total_order_amount': str (
                delivery_item.total_order_amount ( ) ) + " " + delivery_item.harvested_unit_text ( ),
            'ordered_value': delivery_item.ordered_value ( ),
            'harvested_value': delivery_item.harvested_value ( ),
            'unit': delivery_item.order_unit_text ( ),
            'sum_ordered_value': delivery_item.delivery.total_order_value ( ),
            'sum_box_values_and_counts': delivery_item.delivery.box_values_and_counts ( ),
            'sum_harvested_value': delivery_item.delivery.total_harvested_value ( ),
            'box_num': str ( delivery_item.delivery.variant_count ( ) ),
            'relation': str ( delivery_item.harvest_relation ( ) ) + " " + delivery_item.harvested_unit_text ( ),
            'harvested_amount': delivery_item.harvested_amount ( ),
            'ordered_amount': delivery_item.total_order_amount ( ),
            'under_error': delivery_item.under_error ( ),
            'over_error': delivery_item.over_error ( ),
            'variants':variants
            }
    return HttpResponse ( simplejson.dumps ( data ) )


class reset_price(View):
    def post(self, request):
        di = get_object_or_404 ( DeliveryItem, pk=self.request.POST['pk'] )
        listed_price = di.listed_price()
        di.price = listed_price.price
        di.price_type = listed_price.unit
        di.save()

        return values_for_delivery(request)

class delivery_item_edit_price(View):
    def post(self,request):
        delivery_item = get_object_or_404(DeliveryItem, pk=request.POST['pk'])
        price = float(request.POST['value[amount]'])
        delivery_item.price = price

        if 'value[unit]' in request.POST:
            unit = request.POST['value[unit]']
            delivery_item.price_type = unit


        delivery_item.save()
        return HttpResponse ( "" )

class delivery_item_edit_amount(View):
    def post(self,request):
        delivery_item = get_object_or_404(DeliveryItem, pk=request.POST['pk'])
        amount = float(request.POST['value[amount]'])
        delivery_item.order_amount = amount

        if 'value[unit]' in request.POST:
            unit = request.POST['value[unit]']
            delivery_item.amount_unit = unit


        delivery_item.save()
        return HttpResponse ( "" )

class values_for_deliveryitem(View):


    def post(self,request):
        return values_for_delivery ( request )

class delivery_edit_date(View):
    def post(self,request):
        delivery = get_object_or_404(Delivery, pk=request.POST['pk'])
        d = datetime.strptime(request.POST['value'], '%Y-%m-%d')
        delivery.date=d
        delivery.save()
        return HttpResponse ("")

class delivery_variant_edit_count(View):
    def post(self,request):
        variant = get_object_or_404(DeliveryVariant, pk=request.POST['pk'])
        count = request.POST['value']
        variant.count=count
        variant.save()
        return HttpResponse ("")


class cropform_price(View):
    def post(self,request):
        pk_cropform,pk_category=request.POST['pk'].split(",")
        cropform = get_object_or_404(CropForm,pk=pk_cropform)
        category = get_object_or_404(CustomerCategory,pk= pk_category)
        price =    float(request.POST['value[amount]'])
        unit="W"
        if 'value[unit]' in request.POST:
            unit = request.POST['value[unit]']

        p = PriceItem(cropform=cropform, customercategory=category,unit=unit, price=price )
        p.save()
        return HttpResponse("")


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

class deliveryitem_order_comment(View):
    def post(self,request):
        deliveryitem = get_object_or_404 ( DeliveryItem, pk=request.POST['pk'] )
        deliveryitem.order_comment = request.POST['value']
        deliveryitem.save()
        return HttpResponse ( "" )

class deliveryitem_delivery_comment ( View ):
    def post(self, request):
        deliveryitem = get_object_or_404 ( DeliveryItem, pk=request.POST['pk'] )
        deliveryitem.delivery_comment = request.POST['value']
        deliveryitem.save ( )
        return HttpResponse ( "" )

class edit_harvest_state(View):
    pass