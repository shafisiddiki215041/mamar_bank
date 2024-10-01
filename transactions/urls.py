from django.urls import path

from .views import DepositMoneyView, WithdrawMoneyView,LoanRequestView, TransactionReportView, LoanListView, PayLoanView, MoneyTransfer

urlpatterns = [
    path('deposit/',DepositMoneyView.as_view(), name = 'deposit_money'),
    path('report/',TransactionReportView.as_view(), name = 'transaction_report'),
    path('withdraw/',WithdrawMoneyView.as_view(), name = 'withdraw_money'),
    path('loan_request/',LoanRequestView.as_view(), name = 'loan_request'),
    path('loans_list/',LoanListView.as_view(), name = 'loan_list'),
    path('loan_pay/<int:loan_id>',PayLoanView.as_view(), name = 'loan_pay'),
    path('money_transfer/',MoneyTransfer.as_view(),name = 'money_transfer'),
]