from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView, View,RedirectView
from extra_views import ModelFormSetView
from django import template

register = template.Library()




from .forms import *
from .models import *
from urllib.parse import quote, unquote
import simplejson

class Beds (ModelFormSetView):
    template_name = 'harvester/beds.html'
    model = Bed
    exclude =[]

class Cultures (ModelFormSetView):
    template_name = 'harvester/cultures.html'
    model=Culture
    exclude = []
    initial = [{'offset':0}]

class DeliveryNew(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        customer = get_object_or_404 ( Customer, pk=self.request.POST['customer'] )
        delivery_date = self.request.POST['date']
        d=DeliverySingle()
        d.delivery_date=delivery_date
        d.customer=customer
        d.save()
        return reverse('delivery-edit', args=[d.pk])

class Delivery(View):
    def get(self, request,pk):
        delivery = get_object_or_404(DeliverySingle,pk=int(pk))
        template = 'harvester/delivery-edit.html'

        cropform_data = {}
        crops = Crop.objects.all()
        crop_data = [{'name':'välj gröda'}]+[{'pk:':crop.pk, 'name':crop.crop} for crop in crops]
        for crop in crops:
            print(dir(crop))
            cropforms = CropForm.objects.filter(crop=crop.pk)

            cf=[]
            for cropform in cropforms.all():
                cf.append({'pk':cropform.pk, 'name':cropform.form_name,'countable':cropform.countable})
            cropform_data[crop.pk]=cf
        context  = {'delivery':delivery, 'crops':[{'pk':None,'crop':'Välj gröda'}]+list(crops), 'cropform_data':simplejson.dumps(cropform_data)}


        return render ( request,
                        template,
                       context )


    def post(self, request, pk):
        cf=get_object_or_404(CropForm, pk=int(request.POST['cropform']))
        d =get_object_or_404(DeliverySingle, pk=pk)
        di = DeliveryItem(delivery=d,
                          cropform = cf,
                          order_amount = float(request.POST['amount']),
                          order_unit   = request.POST['unit'],
                          price=0,
                          price_type="W"
                          )
        di.save()

        print(request.POST)
        return HttpResponseRedirect ( request.path )


class CropList ( ListView ):
    model = Crop
    template_name = 'harvester/crop-list.html'

class CropEdit ( UpdateView ):
    model = Crop
    form_class = CropFormForm
    template_name = 'harvester/crop-edit.html'

    def get_obj(self):
        return self.get_object ( )

    def get(self, request, *args, **kwargs):
        self.object = self.get_obj ( )
        form_class = self.get_form_class ( )
        form = self.get_form ( form_class )
        cropform_form = CropFormFormSet ( instance=self.object )

        return self.render_to_response (
            self.get_context_data ( form=form,
                                    cropform_form=cropform_form,
                                    ) )

    def post(self, request, *args, **kwargs):
        self.object = self.get_obj ( )
        form_class = self.get_form_class ( )
        form = self.get_form ( form_class )
        cropform_form = CropFormFormSet ( self.request.POST )
        if (form.is_valid ( ) and cropform_form.is_valid ( )):
            return self.form_valid ( form, cropform_form )
        else:
            return self.form_invalid ( form, cropform_form )

    def form_valid(self, form, cropform_form):
        self.object = form.save ( )
        cropform_form.instance = self.object
        cropform_form.save ( )
        return HttpResponseRedirect ( self.get_success_url ( ) )

    def form_invalid(self, form, cropform_form):

        return self.render_to_response (
            self.get_context_data ( form=form,
                                    cropform_form=cropform_form
                                    ) )

    def get_success_url(self):
        return reverse ( 'harvest-new' )

    def get_initial(self):
        return {'time': timezone.now ( )}





class DeliveryList ( ListView ):
    template_name = 'harvester/delivery-list.html'
    model = DeliverySingle





class HarvestItemNew (CreateView):
    model = HarvestItem
    form_class = HarvestItemForm
    template_name = 'harvester/delivery-edit-harvests.html'

    def post(self, request, *args, **kwargs):
        self.success_url =  unquote(self.kwargs['url'])

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        id = self.kwargs['pk']
        deliveryitem = get_object_or_404 ( DeliveryItem, pk=id )

        # the actual modification of the form
        form.instance.destination = deliveryitem

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)