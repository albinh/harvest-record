from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Crop
from .models import CropForm
from .models import Culture
from .models import HarvestItem



class HarvestItemForm(ModelForm):
    culture_state = forms.ChoiceField(choices=Culture.HARVEST_CHOICES,initial=2)
    harvest_state = forms.BooleanField(required=False)


    def __init__(self, *args, **kwargs):
       di = kwargs.pop('di')
       super(HarvestItemForm, self).__init__(*args, **kwargs)
       self.fields['culture'].queryset = Culture.objects.filter ( crop=di.cropform.crop )

    class Meta:
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
        }

        model=HarvestItem
        fields = ['harvested_length', 'culture', 'comment', 'weight', 'count']


