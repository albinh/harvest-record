from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Crop, BasketItem, DeliveryBasket
from .models import CropForm
from .models import Culture
from .models import DeliveryItem
from .models import DeliverySingle
from .models import HarvestItem

class CropFormForm(ModelForm):
    class Meta:
        model=Crop
        exclude=[]

class HarvestItemForm(ModelForm):
    culture_state = forms.ChoiceField(choices=Culture.HARVEST_CHOICES)
    harvest_state = forms.BooleanField(initial=False)
    class Meta:
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
        }

        model=HarvestItem
        fields = ['harvested_length', 'culture', 'comment', 'weight', 'count']


CropFormFormSet        = inlineformset_factory(Crop,CropForm,exclude=[],extra=0,can_delete=True)