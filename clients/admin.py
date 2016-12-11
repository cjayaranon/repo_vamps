from django.contrib import admin
from .models import Client, loanApplication, Loan, LoanInformation, payLoan
# Register your models here.



class ClientsAdmin(admin.ModelAdmin):
    list_display = ['cust_number', 'firstname', 'lastname']

class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['app_id', 'client','app_date', 'app_status']

class LoanAdmin(admin.ModelAdmin):
    filter_horizontal = ('loan_information',)

class PayAdmin(admin.ModelAdmin):
    list_display = ['pay_id', 'client', 'pay_amount', 'pay_trans_date', 'pay_type']

            
admin.site.register(Client, ClientsAdmin)
admin.site.register(loanApplication,LoanApplicationAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(LoanInformation)
admin.site.register(payLoan ,PayAdmin)
