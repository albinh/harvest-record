from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import DeliveryItem
from .models import CropForm
from .models import Culture
from .models import Crop
from .models import DeliverySingle
from .models import Customer
import simplejson
from collections import namedtuple
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
class Option:
    def __init__(self,id,name):
        self.id=id
        self.name=name
    def __str__(self):
        return self.name

# class AjaxView(View):
#     ALWAYS = 1
#     IF_MULTIPLE = 2
#     NEVER =3
#     def post(self,request):
#         self.request=request
#
#
#         try:
#             self.data=self.to_hashes(self.get_data())
#         except:
#             self.data=[]
#         u= self.use_neutral()
#         if (u==self.ALWAYS) or ((len(self.data)>1 and u==self.IF_MULTIPLE)):
#             self.data=self.empty()+self.data
#         return HttpResponse ( simplejson.dumps(self.data))
#
#     def empty(self,name="---"):
#         return [{'id': None, 'name': name}]
#
#     def f(self, id):
#         return int ( self.request.POST[id] )
#
#     def to_hash(self, o):
#         return {'id': o.id, 'name': o.__str__ ( )}
#     def to_hashes(self,o):
#         return [self.to_hash(i) for i in o]
#
# class deliveries_new_order_units_for_cropform(AjaxView):
#
#     def get_data(self):
#         try:
#             cf = CropForm.objects.get(pk=self.f('cropform'))
#             d=[Option('W','kg')]
#             if cf.countable:
#                 name = 'st '+cf.form_name
#                 d=d+[Option('U',name)]
#         except:
#             d = [Option ( 'W', '' )]
#         return d
#     def use_neutral(self):
#         return self.NEVER
#
# class deliveries_new_price_units_for_cropform(AjaxView):
#     def get_data(self):
#         try:
#             cf = CropForm.objects.get(pk=self.f('cropform'))
#
#             d=[Option('W','kr/kg')]
#             if cf.countable:
#                 name = 'kr/st '+cf.form_name
#                 d=d+[Option('U',name)]
#         except:
#             d=[Option('W',"")]
#         return d
#     def use_neutral(self):
#         return self.NEVER
#
# class deliveries_new_cropform_for_crop(AjaxView):
#     def get_data(self):
#
#         return CropForm.objects.filter ( crop=self.f ( 'crop' ) ).order_by ( '-is_default' )
#
#     def use_neutral(self):
#         return self.NEVER



class deliveries_harvest_for_delivery(View):
    def post(self,request):
        delivery_item_id = request.POST['id']
        delivery_item    = get_object_or_404 ( DeliveryItem, pk=delivery_item_id )

        data={'harvested_amount': delivery_item.harvested_amount(),
              'unit': delivery_item.order_unit_text(),
              'status':delivery_item.status(),
              'harvest_relation':delivery_item.harvest_relation(),
            'target_amount':delivery_item.order_amount,
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
        price = int(request.POST['value[amount]'])
        delivery_item.price = price

        if 'value[unit]' in request.POST:
            unit = request.POST['value[unit]']
            delivery_item.amount_unit = unit


        delivery_item.save()
        return HttpResponse ( "" )