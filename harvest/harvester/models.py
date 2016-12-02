from django.db import models
from datetime import datetime
from django.db.models import Sum, Max, Min


class Crop (models.Model):
    crop    = models.CharField(max_length=100)
    def __str__(self):
        return '%s' % (self.crop)

class CropForm(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE,related_name="cropforms")
    form_name = models.CharField(max_length=40)
    weight_of_one_unit = models.DecimalField(max_digits=4,decimal_places=2)
    def __str__(self):
        return self.form_name
    countable = models.BooleanField()

    is_default = models.BooleanField(default=False)




class CustomerCategory (models.Model):
    name= models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Customer (models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    category = models.ForeignKey(CustomerCategory, on_delete=models.CASCADE)


class PriceListItem (models.Model):
    category = models.ForeignKey(CustomerCategory, on_delete=models.CASCADE)
    crop_form = models.ForeignKey(CropForm, on_delete=models.CASCADE)

    PRICE_CHOICES = (
        ('W', 'kr/kg'),
        ('U', 'kr/enhet')

    )
    price_type = models.CharField(max_length=1, choices=PRICE_CHOICES, default="W")
    price = models.DecimalField(max_digits=5, decimal_places=2, )

class Bed (models.Model):
    index = models.CharField(max_length=20)
    location = models.CharField(max_length=10)
    length = models.IntegerField()
    def __str__(self):
        return '%s%s' % (self.location,self.index)

class Culture (models.Model):
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    offset = models.IntegerField(default=0)
    length = models.IntegerField()
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    variety = models.CharField(max_length=100)
    def __str__(self):
        return '%s @ %s' % (self.crop, self.bed)
    HARVEST_CHOICES = ((1, 'Ej skördeklar'),
                     (2, 'Skördeklar'),
                     (3, 'Övermogen/slutskördad'),
               )
    harvest_state = models.IntegerField(choices=HARVEST_CHOICES, default=1)


class DeliverySingle (models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    target_date = models.DateField(default=datetime.now)
    delivery_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return '%s (%s)' % (self.customer.name, self.target_date.strftime("%B %d"))






class DeliveryItem (models.Model):
    crop_form = models.ForeignKey(CropForm)
    delivery = models.ForeignKey(DeliverySingle)
    order_amount = models.DecimalField(max_digits=5,decimal_places=1)

    PRICE_CHOICES = (
                    ('W','kr/kg'),
                    ('U','kr/st')
                     )

    UNIT_CHOICES = (
                    ('W','kg'),
                    ('U','st') )

    price_type = models.CharField(max_length=1, choices=PRICE_CHOICES, default="W", null=True)
    order_unit = models.CharField(max_length=1, choices=UNIT_CHOICES,  default="W", null=True)
    closed =     models.BooleanField(default=False)
    price =      models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discount =   models.FloatField(default=0.0)
    order_comment = models.CharField(max_length=100, default="", blank=True)
    delivery_comment = models.CharField(max_length=100, default="", blank=True)

    NOTHING    = 0
    TOO_LITTLE = 1
    OK         = 2
    TOO_MUCH   = 3

    def status(self):
        q = self.harvested_amount()/self.order_amount
        if self.order_unit=="W":
            h=0.1 # allow 10% differ if calculated in weight
        else:
            h=0   # allow no differ if calculated in count


        if q==0:
            return self.NOTHING
        elif q<1-h:
            return self.TOO_LITTLE
        elif q>1+h:
            return self.TOO_MUCH
        else:
            return self.OK


    def is_closed(self):
        return self.closed
    def is_in_progress(self):
        return HarvestItem.objects.filter(destination=self.pk).count()>0 and not self.closed
    def is_not_started(self):
        return HarvestItem.objects.filter(destination=self.pk).count()==0

    def order_unit_text(self):
        if self.order_unit=="W":
            return "kg"
        elif self.order_unit=="U":
            return self.crop_form.form_name
        else:
            raise


    def harvested_amount(self):
        if self.order_unit=="W":
            a= self.harvested_weight()
        else:
            a=self.harvested_count()
        if a==None:
            return 0
        return a

    def harvested_weight (self):
        harvestitems = HarvestItem.objects.filter(destination=self.pk)
        a= harvestitems.aggregate(weight=Sum('weight'))['weight']
        if a==None:
            return 0
        return a

    def harvested_count(self):
        harvestitems = HarvestItem.objects.filter(destination=self.pk)
        a=harvestitems.aggregate(count=Sum('count'))['count']
        if a==None:
            return 0
        return a

class BasketItem (DeliveryItem):
    in_1 = models.BooleanField ( )
    in_2 = models.BooleanField ( )
    in_3 = models.BooleanField ( )
    in_4 = models.BooleanField ( )
    in_5 = models.BooleanField ( )
    in_6 = models.BooleanField ( )
    in_7 = models.BooleanField ( )
    in_8 = models.BooleanField ( )
    each_amount = models.DecimalField(max_digits=5,decimal_places=1)

class DeliveryBasket(DeliverySingle):
    c_1 = models.PositiveSmallIntegerField(default=0)
    c_2 = models.PositiveSmallIntegerField ( default=0 )
    c_3 = models.PositiveSmallIntegerField ( default=0 )
    c_4 = models.PositiveSmallIntegerField ( default=0 )
    c_5 = models.PositiveSmallIntegerField ( default=0 )
    c_6 = models.PositiveSmallIntegerField ( default=0 )
    c_7 = models.PositiveSmallIntegerField ( default=0 )
    c_8 = models.PositiveSmallIntegerField ( default=0 )


class HarvestItem (models.Model):
    harvested_length = models.DecimalField(max_digits=4, decimal_places=1)
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=True)
    destination = models.ForeignKey(DeliveryItem)
    weight = models.DecimalField(max_digits=5,decimal_places=1)
    count = models.DecimalField(max_digits=5, decimal_places=0)
