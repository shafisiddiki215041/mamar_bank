from django.db.models import Sum
from datetime import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .forms import DepositForm, LoanRequest, WithdrawlForm, TransactionForm, TransferForm
from accounts.models import Bank_Status, UserBankAcoount
from .constants import DEPOSIT,WITHDRAWL,LOAN,LOAN_PAID, TRANSFER
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.
def send_transaction_email(user, amount, subject, template):
    
        message = render_to_string(template,{
            'user' : user,
            'amount': amount
        })
        send_email = EmailMultiAlternatives(subject,'',to=[user.email])
        send_email.attach_alternative(message,'text/html')
        send_email.send()

class TransactionCreateMaxin(LoginRequiredMixin, CreateView):
    template_name = 'transaction_form.html'
    model = Transaction
    title = ''
    success_url= reverse_lazy('transaction_report')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account,
        })
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title' :self.title
        })
        return context
    
    
class DepositMoneyView(TransactionCreateMaxin):
    form_class = DepositForm
    title = 'Deposit'
    
    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields =['balance'],
        )
        messages.success(self.request, f"{amount}$ was deposited to your account successfully")
        
        send_transaction_email(self.request.user, amount, "Deposite Message",'deposite_mail.html')
        return super().form_valid(form)

class WithdrawMoneyView(TransactionCreateMaxin):
    form_class = WithdrawlForm
    title = 'Withdrawl Money'
    
    def get_initial(self):
        initial = {'transaction_type': WITHDRAWL}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        latest_transaction = Bank_Status.objects.last()
        if latest_transaction is not None and latest_transaction.is_bankrupt:
            messages.error(self.request, "The bank is bankrupt. No withdrawals can be processed.")
            return redirect('withdraw_money')
        account.balance -= amount
        account.save(
            update_fields =['balance'],
        )
        messages.success(self.request, f"Successfully withdrawn {amount}$ from your account")
        
        send_transaction_email(self.request.user, amount, "Withdrawl Message",'withdrawl_mail.html')
        
        return super().form_valid(form)

class LoanRequestView(TransactionCreateMaxin):
    form_class = LoanRequest
    title = 'Request For Loan'
    
    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        current_loan_count = Transaction.objects.filter(account=self.request.user.account,loan_approved=True, transaction_type=3).count()
        print('Entry')
        if current_loan_count >3:
            print('Entry2')
            return HttpResponse('You have crossed your limits')
        
       
        messages.success(self.request, f"Loan request for {amount} successfully send to admin")
        
        send_transaction_email(self.request.user, amount, "Loan Request Message",'loan_request_mail.html')
        
        return super().form_valid(form)
    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name ="transaction_report.html"
    model = Transaction
    balance =0
    
    def get_queryset(self):
        queryset= super().get_queryset().filter(
            account = self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            
            queryset = queryset.filter(timestamp__date__gte = start_date, timestamp__date__lte = end_date)
            
            self.balance = Transaction.objects.filter(timestamp__date__gte = start_date, timestamp__date__lte = end_date).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
            
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account' :self.request.user.account
        })
        return context
    
class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transaction, id = loan_id)
        
        if loan.loan_approved:
            user_account = loan.account
            if  loan.amount < user_account.balance:
                user_account.balance -=loan.amount
                loan.balance_after_transaction =user_account.balance
                user_account.save()
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect('loan_list')
                
            else:
               messages.error(self.request, f"Loan amount greater than available balance")
               return redirect('loan_list')
 
class LoanListView(LoginRequiredMixin,ListView):
    model = Transaction
    template_name  = "loan_request.html"
    context_object_name = 'loans'
    
    def get_queryset(self):
        user_account = self.request.user.account 
        queryset = Transaction.objects.filter(account=self.request.user.account, transaction_type=3)
        return queryset
    
    
class MoneyTransfer(TransactionCreateMaxin):
    form_class = TransferForm
    title ='Money Transfer'
    
    def get_initial(self):
        initial = {'transaction_type': TRANSFER}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        destination_account = form.cleaned_data.get('account_id')
        account = self.request.user.account
        
        if destination_account:
            account.balance -= amount
            account.save(update_fields =['balance'])
            
            destination_account.balance += amount
            destination_account.save(update_fields =['balance'])            
        send_transaction_email(self.request.user, amount, "Send Money", 'send_money.html')

        send_transaction_email(destination_account.user, amount, "Receive Money", 'send_money.html')           
        messages.success(self.request, f'Successfully transferred {amount}$ to {destination_account}.')
        return super().form_valid(form)