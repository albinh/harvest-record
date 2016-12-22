from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView, View
from extra_views import ModelFormSetView

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

class DeliveryTest(View):
    def get(self, request,pk):
        delivery = get_object_or_404(DeliverySingle,pk=int(pk))
        template = 'harvester/delivery-edit-test.html'

        cropform_data = {}
        #crops with at least one cropform
        crops = Crop.objects.all()
        crop_data = [{'name':'välj gröda'}]+[{'pk:':crop.pk, 'name':crop.crop} for crop in crops]
        for crop in crops:
            print(dir(crop))
            cropforms = CropForm.objects.filter(crop=crop.pk)
            #crop_data.append(crop)
            cf=[]
            for cropform in cropforms.all():
                cf.append({'pk':cropform.pk, 'name':cropform.form_name,'countable':cropform.countable})
            cropform_data[crop.pk]=cf






        #self_url = quote('')
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

class DeliveryMixin:
    form_class = DeliverySingleForm
    template_name = 'harvester/delivery-edit.html'
    def get_delivery_item_formset(self):
        return DeliveryItemFormSet ( instance=self.object)
    def get(self, request, *args, **kwargs):
        self.object = self.get_obj ( )
        form_class = self.get_form_class ( )
        form = self.get_form ( form_class )
        delivery_item_form = self.get_delivery_item_formset()

        for form2 in delivery_item_form.forms:
            if form2.instance.pk:
                form2.fields['crop'].disabled = True
                form2.fields['cropform'].disabled = True
                form2.initial['crop'] = form2.instance.cropform.crop

        return self.render_to_response (
            self.get_context_data ( form=form,
                                    delivery_item_form=delivery_item_form,
                                    ) )

    def post(self, request, *args, **kwargs):
        self.object = self.get_obj ( )
        form_class = self.get_form_class ( )
        form = self.get_form ( form_class )
        delivery_item_form = DeliveryItemFormSet ( self.request.POST, instance=self.object )
        if (form.is_valid ( ) and delivery_item_form.is_valid ( )):
            return self.form_valid ( form, delivery_item_form )
        else:
            return self.form_invalid ( form, delivery_item_form )

    def form_valid(self, form, delivery_item_form):
        self.object = form.save ( )
        delivery_item_form.instance = self.object
        delivery_item_form.save ( )
        return HttpResponseRedirect ( reverse ( 'delivery-list' ) )

    def form_invalid(self, form, delivery_item_form):
        return self.render_to_response (
            self.get_context_data ( form=form,
                                    delivery_item_form=delivery_item_form
                                    ) )

    def get_initial(self):
        return {'time': timezone.now ( )}

class DeliveryEdit ( DeliveryMixin, UpdateView ):
    model = DeliverySingle

    def get_obj(self):
        return self.get_object ( )

class DeliveryBasketEdit (DeliveryEdit):
    model = DeliveryBasket
    form_class = DeliveryBasketForm
    template_name = 'harvester/delivery-basket-edit.html'
    def get_delivery_item_formset(self):
        return BasketItemFormSet ( instance=self.object)

class DeliveryNew ( DeliveryMixin, CreateView ):
    model = DeliverySingle
    form_class = DeliverySingleForm
    template_name = 'harvester/delivery-edit.html'

    def get_obj(self):
        return None

class DeliveryBasketNew(DeliveryNew):
    model = DeliveryBasket
    form_class = DeliveryBasketForm
    template_name = 'harvester/delivery-basket-edit.html'

    def get_delivery_item_formset(self):
        return BasketItemFormSet ( instance=self.object )

class CustomerCategoryList ( ListView ):
    model = CustomerCategory

class CustomerCategoryEdit ( UpdateView ):
    model = CustomerCategory

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




#class HarvestItemUpdate (UpdateView):
   # model = HarvestItem
  #  fields = ['harvested_length','culture','comment','destination','weight','count']
   # template_name = 'harvester/delivery-edit-harvests.html'
    #form = HarvestItemForm


class DeliveryEditHarvests ( View ):
    template_name = 'harvester/delivery-edit-harvests.html'

    def get_deliveryitem(self):
        id = self.kwargs['pk']
        self.deliveryitem = get_object_or_404 ( DeliveryItem, pk=id )

    def get(self, request, *args, **kwargs):
        self.get_deliveryitem ( )



        return render ( request, self.template_name,
                        {'d_pk': self.deliveryitem.id, 'delivery_item': self.deliveryitem, 'formset': formset,
                         'form': form} )

    def post(self, request, *args, **kwargs):
        self.get_deliveryitem ( )
        formset = HarvestItemFormSet ( request.POST, initial=self.initial_data ( ) )
        if formset.is_valid ( ):
            for form2 in formset.forms:
                if form2.has_changed ( ):
                    self.create_or_update ( form2.cleaned_data )
                    if 'culture_state' in form2.changed_data:
                        self.update_culture_state ( form2.cleaned_data )

            return HttpResponse ( "Here's the text of the Web page." )
        else:
            return HttpResponse ( render ( request, self.template_name, {'formset': formset} ) )
