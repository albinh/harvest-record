from django.contrib import admin
from .models import *

# Register your models here.


class CropFormInline(admin.TabularInline):
    model=CropForm


class CropAdmin (admin.ModelAdmin):
    inlines = [
        CropFormInline,
    ]

class PriceListInline(admin.TabularInline):
    model=PriceListItem

class CustomerCategoryAdmin (admin.ModelAdmin):
    inlines = [PriceListInline
    ]

class DeliveryItemInline(admin.TabularInline):
    model=DeliveryItem

class DeliverySingleAdmin(admin.ModelAdmin):
    inlines = [DeliveryItemInline]


admin.site.register(DeliverySingle,DeliverySingleAdmin)
admin.site.register(PriceListItem)
admin.site.register(Culture)
admin.site.register(Bed)
admin.site.register(Crop, CropAdmin)
admin.site.register(Customer)
admin.site.register(HarvestItem)
admin.site.register(CropForm)
admin.site.register(DeliveryItem)
admin.site.register(CustomerCategory, CustomerCategoryAdmin)