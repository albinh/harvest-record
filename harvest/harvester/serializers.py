from rest_framework import serializers
from .models import DeliveryItem, CropForm, Culture, DeliveryVariant, Customer, Bed


class DeliveryItemSerializer(serializers.ModelSerializer):
    cropform = serializers.SlugRelatedField(
        queryset=CropForm.objects.all(), slug_field='form_name'
    )

    ready_cultures = serializers.SerializerMethodField()
    not_ready_cultures = serializers.SerializerMethodField()
    countable = serializers.SerializerMethodField()

    def get_ready_cultures(self,obj):
        cultures = Culture.objects.filter(crop=obj.cropform.crop, harvest_state=2 )
        return [{'pk':culture.pk,'name':culture.bed.__str__()} for culture in cultures]

    def get_not_ready_cultures(self, obj):
        cultures = Culture.objects.filter ( crop=obj.cropform.crop).exclude(harvest_state=2 )
        return [{'pk': culture.pk, 'name': culture.bed.__str__()} for culture in cultures]

    def get_countable(self,obj):
        return obj.cropform.countable

    class Meta:
        model = DeliveryItem
        fields = ('countable', 'pk','cropform','harvested_amount','harvest_remaining','ordered_value', 'order_amount','order_unit','order_unit_text_short','price_unit_text_short','price','price_type','status','order_comment','ready_cultures', 'not_ready_cultures','total_order_amount')

class DeliveryVariantSerializer(serializers.ModelSerializer):
    extempt_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=DeliveryItem.objects.all(), source='extempt')

    included_ids = serializers.SerializerMethodField()
    def get_included_ids(self,obj):
        return [di.pk for di in obj.included()]

    class Meta:
        model = DeliveryVariant

        fields = ('count', 'pk','value','crop_count','extempt_ids','included_ids')

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('name', 'category')

