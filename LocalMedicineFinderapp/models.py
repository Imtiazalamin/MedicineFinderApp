from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUserRegister(AbstractUser):
    user_type = (
        ('buyer', 'buyer'),
        ('seller', 'seller'),
    )
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    address = models.TextField(blank=False, null=False)
    user_type = models.CharField(max_length=10, choices=user_type, default='buyer')

class Pharmacy(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    address = models.TextField()
    city = models.CharField(max_length=100)
    lat = models.FloatField(blank=True, null=True) # map er jonno dorkar hole
    lng = models.FloatField(blank=True, null=True)


class Medicine(models.Model):
    medicine_name = models.CharField(max_length=100) 
    description = models.TextField(max_length=200)
    cetagory = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='medicines')

    
    
class stock(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='stocks')
    medicine_name = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='medicine_stock')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    
        

      
     

    
    

        

    
    





