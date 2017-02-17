from django.db import models
from datetime import datetime
from django.db.models import Sum, Max, Min

class Crop (models.Model):
    crop    = models.CharField(max_length=100)
    def __str__(self):
        return '%s' % (self.crop)

class CustomerCategory (models.Model):
    name= models.CharField(max_length=50)
    def __str__(self):
        return self.name

    def has_price_for(self,cropform):
        return PriceItem.objects.filter(customercategory=self, cropform=cropform).exists()


class CropForm(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE,related_name="cropforms")
    form_name = models.CharField(max_length=40)
    weight_of_one_unit = models.DecimalField(max_digits=4,decimal_places=2)
    def __str__(self):
        return self.form_name
    countable = models.BooleanField()

    is_default = models.BooleanField(default=False)
    prices = models.ManyToManyField ( CustomerCategory, through='PriceItem' )



class Customer (models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    category = models.ForeignKey(CustomerCategory, on_delete=models.CASCADE)

class PriceListItem (models.Model):
    category = models.ForeignKey(CustomerCategory, on_delete=models.CASCADE)
    cropform = models.ForeignKey(CropForm, on_delete=models.CASCADE)

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


class Delivery (models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    target_date = models.DateField(default=datetime.now)
    delivery_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return '%s (%s)' % (self.customer.name, self.target_date.strftime("%B %d"))

    DELIVERY_TYPES = (
        ('N','normal'),
        ('B','box')
    )

    type = models.CharField(max_length=1,choices=DELIVERY_TYPES,default='N')

    def get_state(self):
        if self.delivery_date:
            return "delivered"
        elif self.deliveryitem_set.exclude(state='N').exists():
            return "in_progress"
        else:
            return "not_started"

    def save(self, force_insert=False, force_update=False):
        is_new = self.pk is None
        super(Delivery, self).save(force_insert, force_update)
        if is_new:
            DeliveryVariant.objects.create(delivery=self, count=1)

    def total_order_value(self):
        sum=0
        for di in self.deliveryitem_set.all():
            sum=sum+di.ordered_value()
        return sum
    def total_harvested_value(self):
        sum=0
        for di in self.deliveryitem_set.all():
            sum=sum+di.harvested_value()
        return sum

    def box_values_and_counts(self):
        d=[]
        for v in self.deliveryvariant_set.all():
            d.append({ 'count':v.crop_count(),'value':v.value(),'pk':v.pk   })
        return d

    def variant_count(self):
        return self.deliveryvariant_set.count()

    def completed_items(self):
        return self.deliveryitem_set.filter(state='C')

    def uncompleted_items(self):
        return self.deliveryitem_set.exclude(state='C')

class DeliveryItem (models.Model):
    cropform = models.ForeignKey(CropForm)
    delivery = models.ForeignKey(Delivery)
    order_amount = models.DecimalField(max_digits=5,decimal_places=1)

    PRICE_CHOICES = (
                    ('W','kr/kg'),
                    ('U','kr/st')
                     )

    UNIT_CHOICES = (
                    ('W','kg'),
                    ('U','st') )

    STATES = (
        ('N','ej påbörjad'),
        ('P','påbörjad'),
        ('C','färdig')    )

    state      = models.CharField(max_length=1, choices=STATES, default='N')

    price_type = models.CharField(max_length=1, choices=PRICE_CHOICES, default="W", null=True)
    order_unit = models.CharField(max_length=1, choices=UNIT_CHOICES,  default="W", null=True)
    closed =     models.BooleanField(default=False)
    price =      models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discount =   models.FloatField(default=0.0)
    order_comment = models.CharField(max_length=100, default="", blank=True)
    delivery_comment = models.CharField(max_length=100, default="", blank=True)

    def ordered_value(self):
        if self.order_unit=='W':
            if self.price_type=='W':
                return self.total_order_amount()*self.price
            elif self.price_type=='U':
                return self.total_order_amount()/self.cropform.weight_of_one_unit*self.price
        elif self.order_unit=='U':
            if self.price_type=='W':
                return self.total_order_amount()*self.cropform.weight_of_one_unit*self.price
            elif self.price_type=='U':
                return self.total_order_amount()*self.price

    def harvested_value(self):
        if self.price_type=='W':
            return self.harvested_amount()*self.price
        elif self.price_type=='U':
            return self.harvested_count()*self.price

    def box_value(self):
        if self.order_unit == 'W':
            if self.price_type == 'W':
                return self.order_amount  * self.price
            elif self.price_type == 'U':
                return self.order_amount / self.cropform.weight_of_one_unit * self.price
        elif self.order_unit == 'U':
            if self.price_type == 'W':
                return self.order_amount  * self.cropform.weight_of_one_unit * self.price
            elif self.price_type == 'U':
                return self.order_amount  * self.price


    def harvest_relation(self):
        return str(self.total_order_amount()-self.harvested_amount())+" "+self.harvested_unit_text()

    NOTHING    = 0
    TOO_LITTLE = 1
    OK         = 2
    TOO_MUCH   = 3

    def status(self):
        q = self.harvested_amount()/self.total_order_amount()
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
            return self.cropform.form_name
        else:
            raise

    def harvested_unit_text(self):
        if self.order_unit=="W":
            return "kg"
        elif self.order_unit=="U":
            return "st"
        else:
            raise

    def price_unit_text(self):
        if self.order_unit=="W":
            return "kr/kg"
        elif self.order_unit=="U":
            return "kr/"+self.cropform.form_name
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
    def total_order_amount(self):
        count = 0
        variants = DeliveryVariant.objects.filter(delivery=self.delivery)
        for variant in variants:
            if not variant.extempt.filter(id=self.pk).exists():
                count = count + variant.count
        return self.order_amount*count


    def variants(self):
        variants = self.delivery.deliveryvariant_set.all()
        v=[]
        j=0
        for variant in variants:
            i=0
            if not variant.extempt.filter ( id=self.pk ).exists ( ):
                i=1

            c=chr(ord('A')+j)
            j=j+1
            v.append({'name':c,'included':i,'variant':variant})
        return v
    def listed_price(self):
        try:
            pi=PriceItem.objects.get(customercategory=self.delivery.customer.category, cropform=self.cropform)
        except:
            pi=PriceItem(price=0,unit="W")
        return pi
    def is_price_as_listed(self):
        pi=self.listed_price()
        return pi.price==self.price and pi.unit==self.price_type




class PriceItem (models.Model):
    customercategory = models.ForeignKey(CustomerCategory)
    cropform         = models.ForeignKey(CropForm)
    price            = models.DecimalField(max_digits=5,decimal_places=2)

    PRICE_CHOICES = (
        ('W', 'kr/kg'),
        ('U', 'kr/st')
    )
    unit     = models.CharField(max_length=1, choices=PRICE_CHOICES, default="W", null=True)


class DeliveryVariant (models.Model):
    delivery     = models.ForeignKey(Delivery)
    count        = models.DecimalField(max_digits=5, decimal_places=0)
    extempt      = models.ManyToManyField(DeliveryItem)
    def value(self):
        value=0
        for di in self.delivery.deliveryitem_set.all():
            if not di in self.extempt.all():
                value=value+di.box_value()

        return value

    def crop_count(self):
        count=0
        for di in self.delivery.deliveryitem_set.all():
            if not di in self.extempt.all():
                count=count+1

        return count

class HarvestItem (models.Model):
    harvested_length = models.DecimalField(max_digits=4, decimal_places=1)
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=True)
    destination = models.ForeignKey(DeliveryItem)
    weight = models.DecimalField(max_digits=5,decimal_places=1)
    count = models.DecimalField(max_digits=5, decimal_places=0,blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True)
