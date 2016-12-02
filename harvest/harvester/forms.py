from django import forms

from django.forms import ModelChoiceField
from .models import Crop, BasketItem, DeliveryBasket
from .models import CropForm
from .models import Culture
from .models import DeliverySingle
from .models import HarvestItem
from .models import DeliveryItem
import floppyforms


from django.forms import ModelForm
from clever_selects.form_fields import ChainedModelChoiceField
from clever_selects.form_fields import ChainedChoiceField
from clever_selects.forms import ChainedChoicesForm
from clever_selects.forms import ChainedChoicesModelForm
from django.forms.models import inlineformset_factory, modelformset_factory, formset_factory
from django.urls import reverse_lazy



class HarvestItemFormUpdate(ModelForm):
    # fields = ['culture', 'weight','count','comment','time']
    error_css_class = "uk-form-danger"
    class Meta:
        model = HarvestItem
        fields = ['culture', 'harvested_length', 'comment', 'destination','weight','count']

        widgets = {
            'comment': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
        }

class DeliverySingleForm(ModelForm):

    class Meta:
        model = DeliverySingle
        fields = ['customer','target_date']


class DeliveryBasketForm(ModelForm):

    class Meta:
        model = DeliveryBasket
        exclude=[]

class DeliveryItemForm(ModelForm):
    crop = forms.ModelChoiceField(queryset=Crop.objects.all())
    class Meta:
        exclude = []
        model = DeliveryItem

class BasketItemForm(ModelForm):
    crop = forms.ModelChoiceField(queryset=Crop.objects.all())
    class Meta:
        exclude = []
        model = BasketItem

class CropFormForm(ModelForm):
    class Meta:
        model=Crop
        exclude=[]

class DeliveryItemHarvestForm(ModelForm):
    class Meta:
        model=DeliveryItem
        fields=['delivery_comment','closed']

class HarvestItemForm(ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    culture_id =  forms.IntegerField(widget=forms.HiddenInput())
    culture_name = forms.CharField ( disabled=True,required=False)
    culture_state = forms.TypedChoiceField(coerce=int, choices=Culture.HARVEST_CHOICES)
    i = forms.ModelChoiceField(queryset=Culture.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model=HarvestItem
        exclude=['destination','culture']


HarvestItemFormSet     = formset_factory(HarvestItemForm,  extra=200, max_num=1)
BasketItemFormSet    = inlineformset_factory(DeliveryBasket, BasketItem,  form=BasketItemForm, exclude=[], extra=1)

DeliveryItemFormSet    = inlineformset_factory(DeliverySingle, DeliveryItem,  form=DeliveryItemForm, exclude=[], extra=1)
CropFormFormSet        = inlineformset_factory(Crop,CropForm,exclude=[],extra=0,can_delete=True)