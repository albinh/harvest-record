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

class Option:
    def __init__(self,id,name):
        self.id=id
        self.name=name
    def __str__(self):
        return self.name

class AjaxView(View):
    ALWAYS = 1
    IF_MULTIPLE = 2
    NEVER =3
    def post(self,request):
        self.request=request

        print (self.request.POST)

        try:
            self.data=self.to_hashes(self.get_data())
        except:
            self.data=[]
        u= self.use_neutral()
        if (u==self.ALWAYS) or ((len(self.data)>1 and u==self.IF_MULTIPLE)):
            self.data=self.empty()+self.data
        return HttpResponse ( simplejson.dumps(self.data))

    def empty(self,name="---"):
        return [{'id': None, 'name': name}]

    def f(self, id):
        return int ( self.request.POST[id] )

    def to_hash(self, o):
        return {'id': o.id, 'name': o.__str__ ( )}
    def to_hashes(self,o):
        return [self.to_hash(i) for i in o]

class deliveries_new_order_units_for_cropform(AjaxView):

    def get_data(self):
        print ("ASDF")
        try:
            cf = CropForm.objects.get(pk=self.f('crop_form'))
            print (dir(cf))
            d=[Option('W','kg')]
            if cf.countable:
                name = 'st '+cf.form_name
                d=d+[Option('U',name)]
        except:
            d = [Option ( 'W', '' )]
        print (d)
        return d
    def use_neutral(self):
        return self.NEVER

class deliveries_new_price_units_for_cropform(AjaxView):

    def get_data(self):
        print ("ASDF")
        try:
            cf = CropForm.objects.get(pk=self.f('crop_form'))

            print (dir(cf))
            d=[Option('W','kr/kg')]
            if cf.countable:
                name = 'kr/st '+cf.form_name
                d=d+[Option('U',name)]
        except:
            d=[Option('W',"")]
        print (d)
        return d
    def use_neutral(self):
        return self.NEVER

class deliveries_new_crop_form_for_crop(AjaxView):
    def get_data(self):

        return CropForm.objects.filter ( crop=self.f ( 'crop' ) ).order_by ( '-is_default' )

    def use_neutral(self):
        return self.NEVER




