from django.db import models
from django.template.defaultfilters import default
from audioop import reverse
from django.template.base import kwarg_re
from shop.settings import AUTH_USER_MODEL
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length = 128)
    slug = models.SlugField(max_length = 128)
    price = models.FloatField(default = 0.0)
    stock = models.IntegerField(default = 0)
    description = models.TextField(blank=True)
    photo = models.FileField(upload_to='photos')
def __str__(self):
    return self.name

def get_absolute_url(self):
    return reverse("product" , kwargs = {"slug":self.slug})

class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL , on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default = False)
    ordered_date = models.DateTimeField(blank = True , null = True)
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL , on_delete=CASCADE)
    orders = models.ManyToManyField(Order)
    

    
    def __str__(self):
        return self.user.username
    
    


    
    

