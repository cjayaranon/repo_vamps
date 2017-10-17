from django.forms import ModelForm, Textarea
from clients.models import Client, Collateral, client_capital, MAF, ODF, loanApplication, Restruct, payLoanLedger_in, payLoanLedger_over, Loan
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field
from crispy_forms.bootstrap import FormActions, PrependedText, AppendedText
from django import forms

class ClientForm(ModelForm):
    class Meta:

        model = Client
        fields = [
            'firstname',
            'middlename',
            'lastname',
            'age',
            'civil_status',
            'phone_number',
            'address',
            'birthdate',
            'educ_attain',
            'occupation',
            'membership_type',
            'client_id_type',
            'client_id_number',
            'beneficiary',
        ]
        
        widgets = {
        'firstname': forms.TextInput(attrs={'placeholder':'First Name'}),
        'middlename': forms.TextInput(attrs={'placeholder':'Middle Name'}),
        'lastname': forms.TextInput(attrs={'placeholder':'Last Name'}),
        'client_id_number': forms.TextInput(attrs={'placeholder':'ID Number'}),
        'birthdate': forms.TextInput(attrs={'placeholder':'YYYY-MM-DD'})
        }

        labels = {
            'firstname':('First Name'),
            'middlename':('Middle Name'),
            'lastname':('Last Name'),
            'civil_status':('Civil Status'),
            'phone_number':('Phone Number'),
            'birthdate':('Date of Birth'),
            'educ_attain':('Educational Attainment'),
            'membership_type':('Membership Type'),
            'client_id_type':('ID Type'),
            'client_id_number':('ID Number'),
            'client_odf':('ODF'),
            'client_maf':('MAF'),
        }


    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        # self.helper.form_method = 'POST'
        self.helper.form_onkeypress = 'return alpha(event)'
        # self.helper.form_class = 'no-spinners','form-horizontal'
        self.helper.add_input(Submit('submit','Add Client'))
        self.helper.layout = Layout(
            Fieldset(
                'firstname',
                'middlename',
                'lastname',
                'civil_status',
                'phone_number',
                'birthdate',
                'educ_attain',
                'membership_type',
                'client_id_type',
                'client_id_number',
                ),
            )
        layout = helper.layout = Layout()
        for field_name, field in self.fields.items():
                layout.append(Field(field_name, placeholder=field.label))
                helper.form_show_labels = False

class CapitalForm(ModelForm):
    class Meta:
        model = client_capital
        fields = [
        'cap_client',
        'cap_contrib_date',
        'cap_contrib',
        'capital'
        ]

        labels = {
        'cap_client': ('Client Name'),
        'cap_contrib_date': ('Date'),
        'cap_contrib': ('Contribution'),
        'capital': ('Total')
        }

class LoanApplicationForm(ModelForm):
    class Meta:
        model = loanApplication
        fields = [
            'client',
            'app_date',
            'app_kind',
            'app_amount',
            
        ]
        widgets = {
            'app_amount': forms.TextInput,
            
        }



class StructLoanApplicationForm(ModelForm):
    class Meta:
        model = loanApplication
        fields = [
            'client',
            'app_date',
            'app_kind',
            'app_amount',
            'restruct'
            
        ]
        widgets = {
            'app_amount': forms.TextInput,
            
        }



class RestructForm(ModelForm):
    class Meta:
        model = Restruct
        fields = [
            'loan_root',
            'loan_in_interest',
            'loan_in_amount',
            'loan_over_interest',
            'loan_over_amount',
            'restruct_fee',
        ]


class CoMakerForm(ModelForm):
    class Meta:
        model = loanApplication
        fields = [
            'app_comaker'
        ]


class CollateralForm(ModelForm):
    class Meta:
        model = Collateral
        fields = [
        'name',
        'owner',
        'description',
        'val'
        ]

        widgets = {
        'name': forms.TextInput(attrs={'placeholder':'Name'}),
        'description': forms.Textarea(attrs={'placeholder':'Desription'}),
        'val': forms.TextInput(attrs={'placeholder':'Monetary Value'})
        }



class PayLoanForm(ModelForm):
    class Meta:
        model = payLoanLedger_in
        fields = [
        'client',
        'trans_date',
        'reference',
        'debit_loanGranted',
        'credit_payment',
        'int_per_month',
        'total_loan_recievable',
        'loan_pay_type',
        'loan_pay_received_by'
        ]

        widgets = {
        'credit_payment': forms.TextInput,
        'reference': forms.TextInput,
        'loan_pay_received_by': forms.TextInput,
        'loan_pay_received_by': forms.TextInput(attrs={'value':'Bookkeeper'}),
        }

        labels = {
        'client':('Client Name'),
        'trans_date': ('Date of Payment'),
        'reference': ('OR No.'),
        'debit_loanGranted': ('Debit/Loan Granted'),
        'credit_payment': ('Credit/Payment'),
        'int_per_month': ('Interest per Month'),
        'total_loan_recievable': ('Total Loan Receivable'),
        'loan_pay_type': ('Payment Type'),
        'loan_pay_received_by': ('Received By')
        }

        initial = {
        'loan_pay_received_by':'Bookkeeper'
        }



class PayLoanForm_o(ModelForm):
    class Meta:
        model = payLoanLedger_over
        fields = [
        'client',
        'trans_date',
        'reference',
        'debit_loanGranted',
        'credit_payment',
        'int_per_month',
        'total_loan_recievable',
        'loan_pay_type',
        'loan_pay_received_by'
        ]

        widgets = {
        'credit_payment': forms.TextInput,
        'reference': forms.TextInput,
        'loan_pay_received_by': forms.TextInput,
        'loan_pay_received_by': forms.TextInput(attrs={'value':'Bookkeeper'}),
        }

        labels = {
        'client':('Client Name'),
        'trans_date': ('Date of Payment'),
        'reference': ('OR No.'),
        'debit_loanGranted': ('Debit/Loan Granted'),
        'credit_payment': ('Credit/Payment'),
        'int_per_month': ('Interest per Month'),
        'total_loan_recievable': ('Total Loan Receivable'),
        'loan_pay_type': ('Payment Type'),
        'loan_pay_received_by': ('Received By')
        }

        initial = {
        'loan_pay_received_by':'Bookkeeper'
        }


class MAFform(ModelForm):
    class Meta:
        model = MAF
        fields = [
        'maf_client',
        'maf_contrib_date',
        'maf_ref',
        'maf_debit',
        'maf_credit',
        'maf_total'
        ]

        labels = {
        'maf_client': ('Client Name'),
        'maf_contrib_date': ('Date'),
        'maf_ref': ('Reference'),
        'maf_debit': ('Debit'),
        'maf_credit': ('Credit'),
        'maf_total': ('Total')
        }

        initial = {
        'maf_ref':'-'
        }


class ODFform(ModelForm):
    class Meta:
        model = ODF
        fields = [
        'odf_client',
        'odf_contrib_date',
        'odf_ref',
        'odf_debit',
        'odf_credit',
        'odf_total'
        ]

        labels = {
        'odf_client': ('Client Name'),
        'odf_contrib_date': ('Date'),
        'odf_ref': ('Reference'),
        'odf_debit': ('Debit'),
        'odf_credit': ('Credit'),
        'odf_total': ('Total')
        }