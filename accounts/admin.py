from django.contrib import admin
from .models import UserBankAcoount, AddressAcount, Bank_Status
# Register your models here.

admin.site.register(UserBankAcoount)
admin.site.register(AddressAcount)

@admin.register(Bank_Status)
class BankStatusAdmin(admin.ModelAdmin):
    list_display = ['is_bankrupt']
    