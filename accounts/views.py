from django.shortcuts import render,redirect
from django.views.generic import FormView, UpdateView, View
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView,PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from transactions.views import send_transaction_email
from django.contrib import messages
from django.http import HttpResponseRedirect
 
# Create your views here.
class UserRegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)

class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
       
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('profile')
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
            

class PasswordChange(PasswordChangeView):
    template_name = 'accounts/pass_change_email.html'  # Ensure this is correct
    form_class = PasswordChangeForm

    def form_valid(self, form):
        form.save()  # Save the new password
        messages.success(self.request, 'Your password was successfully changed!')
        send_transaction_email(self.request.user, '', "Password Change Notification", 'accounts/pass_email.html')
        return HttpResponseRedirect(self.request.path)
        
      
# def PasswordChange(request):
#     if request.method == 'POST':
#         form= PasswordChangeForm(request.user, data =request.POST)
#         if form.is_valid():
#             form.save()
#             send_transaction_email(request.user, '', "Pass Change Email", 'pass_email.html')
#             messages.success(request, 'Password Update Successfully')
#             update_session_auth_hash(request, form.user)
#             return redirect('pass_change')
#     else:
#         form= PasswordChangeForm(user = request.user)
#     return render(request,'accounts/pass_change_email.html',{'form':form})