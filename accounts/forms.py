from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .constants import ACCOUNT_TYPE, GENDER_TYPE
from .models import UserBankAcoount, AddressAcount

class UserRegistrationForm(UserCreationForm):
    birt_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country= forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ['username','password1','password2','first_name','last_name','email','account_type','birt_date','city','gender','postal_code','country','street_address']
    
    def save(self, commit = True):
        our_user = super().save(commit=False) #ekhon database a data save korbo na
        if commit == True:
            our_user.save() #user model a data save korlam
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            birt_date = self.cleaned_data.get('birt_date')
            city = self.cleaned_data.get('city')
            street_address = self.cleaned_data.get('street_address')
            
            
            AddressAcount.objects.create(
                user = our_user,
                postal_code = postal_code,
                country=country,
                city = city,
                street_address=street_address
            )
            UserBankAcoount.objects.create(
                user = our_user,
                account_type=account_type,
                gender = gender,
                birt_date= birt_date,
                account_number = 100000 + our_user.id
            )
        return our_user
             
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                  'appearance-none block w-full bg-gray-200 '
                  'text-gray-700 border border-gray-200 rounded '
                  'py-3 px-4 leading-tight focus:outline-none '
                  'focus:bg-white focus:border-gray-500'  
                )
            })
            # print(field)
            
class UserUpdateForm(forms.ModelForm):
    birt_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country= forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                  'appearance-none block w-full bg-gray-200 '
                  'text-gray-700 border border-gray-200 rounded '
                  'py-3 px-4 leading-tight focus:outline-none '
                  'focus:bg-white focus:border-gray-500'  
                )
            })
            #jodoi user er account thake those is instance
            if self.instance:
                try:
                    user_account =self.instance.account
                    user_address = self.instance.address
                except UserBankAcoount.DoesNotExist:
                    user_account = None
                    user_address = None
                    
                if user_account:
                    self.fields['account_type'].initial = user_account.account_type
                    self.fields['birt_date'].initial = user_account.birt_date
                    self.fields['gender'].initial = user_account.gender
                    self.fields['street_address'].initial = user_address.street_address
                    self.fields['city'].initial = user_address.city
                    self.fields['postal_code'].initial = user_address.postal_code
                    self.fields['country'].initial = user_address.country                 
                    
    def save(self, commit =True):
        user = super().save(commit=False)
        if commit ==True:
            user.save()
            
            user_account, created = UserBankAcoount.objects.get_or_create(user=user)
            user_address, created =AddressAcount.objects.get_or_create(user = user)
            
            user_account.account_type = self.cleaned_data['account_type']
            user_account.gender = self.cleaned_data['gender']
            user_account.birt_date = self.cleaned_data['birt_date']
            user_account.save()
             
            user_address.street_address = self.cleaned_data['street_address']  
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()
        return user 
                
                    
                    
                    