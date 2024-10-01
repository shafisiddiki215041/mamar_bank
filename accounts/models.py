from django.db import models
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE, GENDER_TYPE
# django amader built in user make korar facility dey

class UserBankAcoount(models.Model):
    user= models.OneToOneField(User, related_name='account',on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10,choices=ACCOUNT_TYPE)
    account_number =models.IntegerField(unique=True)  #account number always different hobe
    birt_date = models.DateField(null=True,blank=True)
    gender = models.CharField(choices=GENDER_TYPE,max_length=10)
    initial_deposit = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0,max_digits=12,decimal_places=2) # ekjon user 12 ta digit user korte parbe and 2 digit after doshomik use korte parbe
    
    def __str__(self):
        return f"{self.account_number}"
    

class AddressAcount(models.Model):
    user = models.OneToOneField(User,related_name='address',on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    country= models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.email
    

    
    
class Bank_Status(models.Model):
    is_bankrupt = models.BooleanField(default=False)
    
    