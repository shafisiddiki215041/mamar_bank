from django.contrib import admin
from django.urls import path, include 
from core.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('',HomeView.as_view(),name ='home'),
    path('transactions/',include('transactions.urls')),
]
