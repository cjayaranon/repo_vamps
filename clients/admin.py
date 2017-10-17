from django.contrib import admin
<<<<<<< HEAD
from .models import Client, client_capital, loanApplication, Loan, payLoanLedger_in, payLoanLedger_over, MAF, ODF, Collateral, Restruct
=======
from .models import Client, loanApplication, Loan, LoanInformation, payLoan
>>>>>>> 549418614833c8e5b4d8caf88e6746fdc1fb1760
# Register your models here.



class ClientsAdmin(admin.ModelAdmin):
    list_display = ['lastname', 'firstname', 'cust_number', 'membership_type', 'client_status']

class ClientCapitalAdmin(admin.ModelAdmin):
	list_display = ['cap_client','cap_id', 'capital', 'cap_contrib_date']

class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['client', 'app_kind', 'app_amount', 'app_date', 'app_status', 'app_id', 'restruct']

class LoanAdmin(admin.ModelAdmin):
    list_display = ['client', 'loan_status', 'interest_rate', 'interest_rate_over', 'id', 'update', 'overdue', 'type_of_loan']

class RestructAdmin(admin.ModelAdmin):
	list_display = ['loan_root', 'loan_in_interest', 'loan_in_amount', 'loan_over_interest', 'loan_over_amount', 'approval_status', 'restruct_status', 'restruct_fee', 'id']

class CollAdmin(admin.ModelAdmin):
	list_display = ['name', 'owner', 'description', 'val']

class PayAdmin_IN(admin.ModelAdmin):
    list_display = ['client', 'trans_date', 'reference', 'debit_loanGranted', 'credit_payment', 'int_per_month', 'total_loan_recievable', 'loan_pay_type', 'loan_pay_id']

class PayAdmin_OVER(admin.ModelAdmin):
    list_display = ['client', 'trans_date', 'reference', 'debit_loanGranted', 'credit_payment', 'int_per_month', 'total_loan_recievable', 'loan_pay_type', 'loan_pay_id',]

class PayMAFAdmin(admin.ModelAdmin):
    list_display = ['maf_client','maf_contrib_date', 'maf_ref', 'maf_debit', 'maf_credit', 'maf_total', 'maf_id']

class PayODFAdmin(admin.ModelAdmin):
    list_display = ['odf_client', 'odf_contrib_date', 'odf_ref', 'odf_debit', 'odf_credit', 'odf_total', 'odf_id']

            
admin.site.register(Client, ClientsAdmin)
admin.site.register(client_capital, ClientCapitalAdmin)
admin.site.register(loanApplication,LoanApplicationAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(Restruct, RestructAdmin)
admin.site.register(Collateral, CollAdmin)
admin.site.register(payLoanLedger_in ,PayAdmin_IN)
admin.site.register(payLoanLedger_over, PayAdmin_OVER)
admin.site.register(MAF, PayMAFAdmin)
admin.site.register(ODF, PayODFAdmin)
