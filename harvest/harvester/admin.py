from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *

# Register your models here.


class CropFormInline(admin.TabularInline):
    model=CropForm


class CropAdmin (ImportExportModelAdmin):

    inlines = [
        CropFormInline,
    ]

class CultureAdmin (ImportExportModelAdmin):
    pass

class BedAdmin (ImportExportModelAdmin):
    pass

class PriceListInline(admin.TabularInline):
    model=PriceItem

class CustomerCategoryAdmin (admin.ModelAdmin):
    inlines = (PriceListInline,)

class DeliveryItemInline(admin.TabularInline):
    model=DeliveryItem

admin.site.register(PriceItem)
admin.site.register(Delivery)

admin.site.register(Culture,CultureAdmin)
admin.site.register(Bed,BedAdmin)
admin.site.register(Crop, CropAdmin)
admin.site.register(Customer)
admin.site.register(HarvestItem)
admin.site.register(CropForm)
admin.site.register(DeliveryItem)
admin.site.register(CustomerCategory, CustomerCategoryAdmin)