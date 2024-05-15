from urllib import request
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum
from django.urls import reverse

# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField( auto_now_add=True)

    class Meta:
        abstract=True

class CarCategory(BaseModel):
    category_name = models.CharField(max_length=100)
    def __str__(self):
        return self.category_name
        
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'


class Car(BaseModel):
    CAR_TYPES = (
        ('U', 'Used'),
        ('N', 'New'),
    )
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE, related_name='cars')
    car_name = models.CharField(max_length=100)
    desc = models.CharField(max_length=500, null=True, blank=True)
    price = models.IntegerField()
    color = models.CharField(max_length=10, null=True, blank=True)
    images = models.ImageField(upload_to='car', blank=True)
    images2 = models.FileField(upload_to='car', null=True, blank=True)
    images3 = models.ImageField(upload_to='car', null=True, blank=True)
    images4 = models.ImageField(upload_to='car', null=True, blank=True)
    images5 = models.ImageField(upload_to='car', null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,  related_name = 'cars')
    car_type = models.CharField(max_length=1, null=False, choices=CAR_TYPES, default='U')

    def __str__(self):
        return self.car_name
    def get_absolute_url(self):
    #return reverse('article-detail', args=(str(self.id)) )
        return reverse('sell')




class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,  related_name = 'carts')
    is_paid = models.BooleanField(default=False)
    

    # def sub_cart_total(self):
    #     return 
    
    
    @property
    def sub_cart_total(self):
        t= (CartItems.objects.filter(cart = self).aggregate(Sum('car__price'))['car__price__sum'])
        
        if t==0:
            return 0
        else:
            return t
        
    @property
    def tax_cart_total(self):
        print(CartItems)
        car_price_sum = (CartItems.objects.filter(cart = self).aggregate(Sum('car__price'))['car__price__sum']) 
        if car_price_sum is None:
            car_price_sum = 0
        # t= (CartItems.objects.filter(cart = self).aggregate(Sum('car__price'))['car__price__sum'])*0.5
        t =car_price_sum*0.05
        t=int(t)
        if t is None:
            return 0.0
        if t==0:
            return 0
            
        else:
            return t
    
    @property
    def get_cart_total(self):
        t = self.sub_cart_total + self.tax_cart_total + 999
        if t==0:
            return 0
        else:
            return t
    
    
    
    

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name= 'cart_items')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)


class ShippingAddress(models.Model):
    username = models.CharField(max_length=500, null=True, blank= True)
    address = models.CharField(max_length=50, null=True, blank= True)
    city = models.CharField(max_length=50, null=True, blank= True)
    state = models.CharField(max_length=50, null=True, blank= True)
    zip = models.CharField(max_length=50, null=True, blank= True)
    date_added = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=50, null=True, blank= True)
    days = models.IntegerField(null=True, blank=True, default=1)
    def __str__(self):
        return self.address