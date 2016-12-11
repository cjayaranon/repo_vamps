from django.forms import ModelForm
from clients.models import Client
from clients.models import loanApplication, payLoan
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
            # 'client_status',
            'capital',
            'client_id_type',
            'client_id_number',
            'client_odf',
            'client_maf',
            'beneficiary',
        ]
        
        widgets = {
        'capital': forms.TextInput,
        'client_odf': forms.TextInput,
        'client_maf': forms.TextInput,
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
            # 'client_status':('Client Status'),
            'client_id_type':('ID Type'),
            'client_id_number':('ID Number'),
            'client_odf':('ODF'),
            'client_maf':('MAF'),
        }

    def __init__(self, *args, **kwargs):
        # request = kwargs.pop('request')
        super(ClientForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        # self.helper.form_method = 'POST'
        self.helper.form_onkeypress = 'return alpha(event)'
        self.helper.form_class = 'no-spinners','form-horizontal'
        self.helper.show_form_labels = False
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
                'client_odf',
                'client_maf'
                ),
            )
        layout = helper.layout = Layout()
        for field_name, field in self.fields.items():
                layout.append(Field(field_name, placeholder=field.label))
                helper.form_show_labels = False
        
class LoanApplicationForm(ModelForm):
    class Meta:
        model = loanApplication
        fields = [
            'client',
            'app_id',
            'app_date',
            # 'app_status',
            'app_kind',
            'app_amount',
            'app_comaker',
            
        ]
        widgets = {
            'app_amount': forms.TextInput,

        }
        labels = {
            'client': ('Client Name'),
            # 'app_status': ('Loan Status'),
            'app_kind': ('Type of Loan'),
            'app_amount': ('Loan amount'),
            'app_comaker': ('Loan comaker'),
        }

class PayLoanForm(ModelForm):
    class Meta:
        model = payLoan
        fields = [
        'client',
        'pay_amount',
        'pay_trans_date',
        'pay_type',
        'pay_for'
        ]

        widgets = {
        'pay_amount': forms.TextInput,
        }

        labels = {
        'client': ('Client Name'),
        'pay_amount': ('Amount'),
        'pay_trans_date': ('Date of Payment'),
        'pay_type': ('Payment Type'),
        'pay_for': ('Payment for')
        }