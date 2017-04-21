import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, UpdateView, ListView, View,RedirectView
from django.views.generic import DetailView
from extra_views import ModelFormSetView
from rest_framework.renderers import JSONRenderer

from .serializers import DeliveryItemSerializer

from .forms import *
from .models import *
from datetime import datetime, timedelta
from urllib.parse import quote, unquote
from rest_framework.response import Response
import simplejson

def save_price_from_delivery_item_to_pricelist(request):
    if request.method == 'POST':
        di = get_object_or_404 ( DeliveryItem, pk=request.POST['pk'])
        price = float(request.POST['price'])
        price_type = request.POST['price_type']


        pi = PriceItem(price=price, unit=price_type, customercategory=di.delivery.customer.category, cropform=di.cropform)
        pi.save()
        return HttpResponse("")


class DeliveryNew ( RedirectView ):
    http_method_names=['post']
    def get_redirect_url(self, *args, **kwargs):
        customer = get_object_or_404 ( Customer, pk=self.request.POST['customer'] )
        date = self.request.POST['date']

        d = Delivery ( )
        d.date = date
        d.customer = customer
        d.save ( )
        return reverse ( 'delivery-edit', args=[d.pk] )

class CustomerNew(View):
    def post(self,request):
        c=Customer()
        c.name=request.POST['name']
        c.category=get_object_or_404(CustomerCategory,pk=request.POST['category'])
        c.save()
        return redirect(reverse('customer-list'))


class CustomerList(ListView):
    model = CustomerCategory
    template_name = 'harvester/customers-list.html'
    def categories(self):
        return CustomerCategory.objects.all()

class DeliveryVariantNew(RedirectView):
    http_method_names = ['post']
    def get_redirect_url(self,*args,**kwargs):
        delivery = get_object_or_404 ( Delivery, id = self.kwargs['pk'])

        v = DeliveryVariant()
        v.count=0
        v.delivery=delivery
        v.save()
        return reverse ( 'delivery-edit', args=[delivery.pk] )

class HarvestsView(View):

    def get(self,request,days):
        days = max(int(days),0)
        dis = DeliveryItem.objects.exclude(delivery__state='C').filter( delivery__date__lte=datetime.now()+timedelta(days=days)).order_by('delivery__date')
        template= 'harvester/harvests.html'
        context= {'deliveryitems':dis}

        return render ( request,
                        template,
                        context )


class DeliveryView(View):
    def crops(self):

        #todo: sortera med grödor som har aktiva kulturer först, därefter grödor
        #todo: som är ännu ej skördade, därefter slutskördade
        HARVEST_CHOICES = ((1, 'Ej skördeklar'),
                           (2, 'Skördeklar'),
                           (3, 'Övermogen/slutskördad'))
        def a(cultures):
            c=[]
            for culture in cultures:

                c.append ( {'pk': culture.crop.pk, 'name': culture.crop.crop} )
            return c

        ready_crops =   a(Culture.objects.filter(harvest_state=2))

        not_ready_all = a(Culture.objects.filter(harvest_state=1))

        finished_all =  a(Culture.objects.filter(harvest_state=2))

        if not_ready_all==None:
            not_ready_all=[]

        if finished_all==None:
            finished_all=[]

        not_ready = [i for i in not_ready_all if i not in ready_crops]
        finished = [i for i in finished_all if i not in ready_crops]

        return {'not_ready':not_ready,'ready':ready_crops,'finished':finished}

    def get(self,request,pk):
        delivery = get_object_or_404(Delivery,pk=int(pk))

    def cropforms(self):
        #todo: sortera cropforms. Först de som har ett pris i prislistan. Sedan övriga med parantes runt.
        #todo: finns det bara en med pris - sätt den som default.
        cropform_data = {}

        for crop in Crop.objects.all():
            cropforms = CropForm.objects.filter(crop=crop.pk)

            priced = [cf for cf in cropforms if self.delivery.customer.category.has_price_for(cf) ]
            not_priced = [cf for cf  in cropforms if cf not in priced]

            def a(l):
                return [{'pk': cropform.pk,
                  'name': cropform.form_name,
                  'countable': cropform.countable}
                 for cropform in l]



            cropform_data[crop.pk] =  {'priced':a(priced),'not_priced':a(not_priced)}
        return cropform_data
    def get(self, request,pk):
        self.delivery = get_object_or_404(Delivery,pk=int(pk))

        template = 'harvester/delivery-edit.html'

        v=[{'name':chr(ord('A')+i),'variant':v} for i,v in enumerate(self.delivery.deliveryvariant_set.all())]

        d=dir(self.delivery)



        context  = {'delivery':self.delivery,
                    'crops':self.crops(),
                    'cropform_data':simplejson.dumps(self.cropforms()),
                    'variants':v
                    }

        return render ( request,
                        template,
                        context )



    # Skapa en ny DeliveryItem
    def post(self, request, pk):
        # TODO: ska skapa DeliveryItem verkligen vara här?

        cropform=get_object_or_404(CropForm, pk=int(request.POST['cropform']))
        delivery =get_object_or_404(Delivery, pk=pk)

        di = DeliveryItem(delivery=delivery,
                          cropform = cropform,
                          order_amount = float(request.POST['amount']),
                          order_unit   = request.POST['unit'],
                          price=0,
                          price_type="W"  # TODO: sätt pris och pristyp efter prislista
                          )
        p = di.listed_price()
        di.price=p.price
        di.price_type=p.unit
        di.save()

        # skicka tillbaka till föregående
        return HttpResponseRedirect ( request.path )

#använd post
class DeliverySetDelivered( RedirectView):
    http_method_names = ['post']
    def get_redirect_url(self, *args, **kwargs ):
        id = self.kwargs['pk']
        delivery = get_object_or_404 ( Delivery, pk=id )
        date = self.request.POST['date']

        delivery.date=date
        delivery.state = "D"
        delivery.save()

        for di in delivery.deliveryitem_set.all():
            di.state="C"
            di.save()

        return reverse("delivery-spec", args=[delivery.pk])


#använd post
class CropNew(RedirectView):
    http_method_names = ['post']
    def get_redirect_url(self,*args,**kwargs):
        name = self.request.POST['name']

        cf=Crop.objects.create(crop=name)
        return(reverse('crops-prices'))

#använd post
class CustomerCategoryNew(RedirectView):
    http_method_names = ['post']
    def get_redirect_url(self,*args,**kwargs):
        name = self.request.POST['name']

        cf=CustomerCategory.objects.create(name=name)
        return(reverse('crops-prices'))

#använd post
class cropform_new(RedirectView):
    http_method_names = ['post']
    def get_redirect_url(self,*args,**kwargs):
        crop = get_object_or_404( Crop, pk=self.request.POST['cropid'])
        name = self.request.POST['name']
        countable = 'countable' in self.request.POST
        weight_of_one_unit = float(self.request.POST['weightofoneunit'])

        cf=CropForm.objects.create(form_name=name, countable=countable, weight_of_one_unit=weight_of_one_unit, crop=crop)
        return(reverse('crops-prices'))



class CropsPrices(View):
    def get(self,request):
        template = "harvester/cropsprices.html"
        categories = []
        crops = []
        for category in CustomerCategory.objects.all():
            categories.append({'category':category.name,
                               'customers':category.customer_set.all()
                               })

        for crop in Crop.objects.all():
            cropforms = []
            for cropform in crop.cropforms.all():
                prices = []
                for category in CustomerCategory.objects.all():
                    pi = PriceItem.objects.filter(customercategory=category,cropform=cropform).first()
                    prices.append( {'priceitem':pi, 'category':category } )
                cropforms.append (
                    {
                        "prices":prices,
                        "cropform":cropform
                    }

                )
            crops.append ( {
                "crop":crop,
                "cropforms":cropforms
            })
        context  = {
                    'categories':categories,
                    'crops':crops,

                    }

        return render ( request,
                        template,
                        context )


class DeliverySpec ( DetailView ):
    model = Delivery
    template_name = "harvester/delivery-spec.html"



class DeliveryList ( ListView ):
    template_name = 'harvester/delivery-list.html'
    model = Delivery





#TODO: använd post
class HarvestItemDelete(RedirectView):
    http_method_names = ['post']
    def get_redirect_url(self, *args, **kwargs):
        id = self.kwargs['pk']
        harvestitem = get_object_or_404 ( HarvestItem, pk=id )
        deliveryitem = harvestitem.destination
        harvestitem.delete()
        return reverse("delivery-edit", args=[deliveryitem.delivery.pk])


#TODO: använd post
class DeliveryDelete( RedirectView ):
    http_method_names = ['post']
    def get_redirect_url(self, *args, **kwargs):
        id = self.kwargs['pk']
        deliverysingle = get_object_or_404 ( Delivery, pk=id )
        deliverysingle.delete()
        return reverse("delivery-list")

#TODO: använd post
class DeliveryItemDelete(RedirectView):
    http_method_names = ['post']
    def get_redirect_url(self, *args, **kwargs):
        id = self.kwargs['pk']
        deliveryitem=get_object_or_404 ( DeliveryItem, pk=id )
        delivery = deliveryitem.delivery
        deliveryitem.delete()
        return reverse("delivery-edit", args=[delivery.pk])


# class HarvestItemUpdate(UpdateView):
#     model = HarvestItem
#     form_class = HarvestItemForm
#     template_name = 'harvester/delivery-edit-harvests.html'
#
#     def deliveryitem(self):
#         id = self.kwargs['pk']
#         return get_object_or_404 ( HarvestItem, pk=id ).destination
#
#     def prev_harvests(self):
#         pk = self.kwargs['pk']
#         return HarvestItem.objects.filter(destination_id=pk)
#
#     def get_success_url(self):
#         return unquote ( self.kwargs['url'] )

class HarvestItemNew (CreateView):
    model = HarvestItem
    form_class = HarvestItemForm
    template_name = 'harvester/delivery-edit-harvests.html'

    def di_data(self):

        data= DeliveryItemSerializer ( self.deliveryitem() ).data
        return JSONRenderer ( ).render ( data )

        #return json.dumps(DeliveryItemSerializer ( self.deliveryitem()).data)


    def deliveryitem(self):
        id = self.kwargs['pk']
        return get_object_or_404 ( DeliveryItem, pk=id )

    def prev_harvests(self):
        pk = self.kwargs['pk']
        return HarvestItem.objects.filter(destination_id=pk)

    def get_form_kwargs(self):
        kwargs = super(HarvestItemNew, self).get_form_kwargs()
        kwargs['di'] = self.deliveryitem()
        return kwargs


    def post(self, request, *args, **kwargs):
        self.success_url =  unquote(self.kwargs['url'])

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # the actual modification of the form
        form.instance.destination = self.deliveryitem()


        form.fields["culture"].queryset = Culture.objects.filter ( crop=form.instance.destination.cropform.crop )

        if form.is_valid():
            if form.cleaned_data["harvest_state"]:
                form.instance.destination.state='P'
                form.instance.destination.save()
            else:
                form.instance.destination.state = 'C'
                form.instance.destination.save ( )
            form.instance.destination.delivery.state = 'P'
            form.instance.destination.delivery.save()
            return self.form_valid(form)
        else:
             return self.form_invalid(form)


