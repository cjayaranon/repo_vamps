import datetime, pdfkit

# Create your views here.
#views.py
from vamps.forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.conf import settings
from django.views.generic import TemplateView
from clients.models import Client, Loan, LoanInformation, loanApplication, payLoan
from clients.forms import ClientForm, LoanApplicationForm, PayLoanForm

User = get_user_model()


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            #email=form.cleaned_data['email'],
            #position=form.cleaned_data['position'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            )
            user.position=form.cleaned_data['position']
            user.save()


            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    auth_logout(request)
    return render_to_response(
        'logout.html',
        )


def restricted(request):
    auth_logout(request)
    return render_to_response(
        'restriction.html',
        )
 
 
@login_required(login_url='/')
def home(request):
    return render_to_response(
    'home.html',
    { 'user': request.user }
    )
    return render_to_response('base.html', {'user': request.user})




def login_user(request):

    if request.method == "GET":
        
        if not request.user.is_authenticated():
            
            return render(request, 'login.html', {})

        if request.user.position == 'Bookkeeper':
            return HttpResponseRedirect(reverse('book_menu'))
        elif request.user.position == 'Admin':
            return HttpResponseRedirect(reverse('admin_page'))
        elif request.user.position == 'Cashier':
            return HttpResponseRedirect(reverse('cashier_menu'))

        return HttpResponseRedirect('logout')

    elif request.method == "POST":
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            
            if user.is_active:
                
                auth_login(request, user)
                if user.position == 'Admin':
                    
                    return HttpResponseRedirect('web-admin/')
                elif user.position == 'Cashier':
                    return HttpResponseRedirect('cashier/')
                elif user.position == 'Bookkeeper':
                    return HttpResponseRedirect('bookkeeper/')
            else:
                
                return render(request, 'login.html', {'error': 'Disabled Account'})
        else:
            
            return render(request, 'login.html', {'error': 'Invalid Credentials'})
    return render(request,'login.html', {})


def search2(request):
    if request.method_decorator == "GET":
        return HttpResponseRedirect('client_list')
    
 

class cashier(View):
    """page sa cashier"""
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        context={}
        if request.user.position == 'Cashier':
            return render(request, "cashier_menu.html", context)
        else:
            return render(request, "restriction.html", context)
        
        
        
class bookkeeper(View):
    """page para sa bookkeeper"""
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        context={}
        if request.user.position == 'Bookkeeper':
            return render(request, "bookkeeper_menu.html", context)
        else:
            return render(request, "restriction.html", context)


class add_new_client(View):
    """para sa pag add new client/member"""

    def get(self, request, *arg, **kwargs):
        request = kwargs.pop('request')
        self.user = request.user
        form = ClientForm(request.POST, request=request)
        context={}
        context['form']=ClientForm(request=request)
        return render(request, "bookkeeper_new_client.html", context)

class admin_page(View):
    """para sa page sa admin"""

    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        context={}
        if request.user.position == 'Admin':
            return render(request, "admin_menu.html", context)
        else:
            return render(request, "restriction.html", context)
        


class UsersView(TemplateView):
    template_name = 'user_list.html'
    
    def get_context_data(self,**kwargs):
        context = super(UsersView,self).get_context_data(**kwargs)
        context['object_list'] = Client.objects.all()
        return context


class ClientView(TemplateView):
    template_name = 'client_list.html'
    
    def get_context_data(self,**kwargs):
        context = super(ClientView,self).get_context_data(**kwargs)
        context['object_list'] = Client.objects.all()
        return context


class Modify(View):

    def post(self, request, *args, **kwargs):
        logged_user = request.user
        if request.POST['submit'] == 'changeuser':
            logged_user = request.user
            logged_user.first_name = request.POST.get('first_name')
            logged_user.last_name = request.POST.get('last_name')
            logged_user.save()
            alert = {'message': 'Successfuly Registered'}
            return render(request, 'editprofile.html', alert,)
        elif request.POST['submit'] == 'changepass':
            curr_pass = request.POST.get('curr_pass')
            conf_pass = request.POST.get('conf_pass')
            new_pass = request.POST.get('new_pass')
            auth_user = authenticate(username=logged_user, password=curr_pass)
            if new_pass != conf_pass:
                password_error = {'password_error': 'Password Does Not Match'}
                return render(request, 'editprofile.html', password_error,)
            if auth_user is not None:
                logged_user.set_password(conf_pass)
                logged_user.save()
                updated = {'success_pass': 'Password Changed'}
                return render(request, 'editprofile.html', updated,)
            else:
                password_error = {'password_error': 'Invalid Password'}
                return render(request, 'editprofile.html', password_error,)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'editprofile.html', {},)



class add_client(View):
    
    def post(self, request, *args, **kwargs):
        forms = ClientForm(request.POST)
        form = ClientForm()
        if forms.is_valid():
            success = 'Client created successfuly'
            forms.save()
            return render(request, 'bookkeeper_new_client.html', {'success':success, 'form': form})
        else:
            error = 'Please fill the form properly'
            print forms.errors
            return render(request, 'bookkeeper_new_client.html', {'error':error, 'form': form})


    def get(self, request, *args, **kwargs):
        
        # self.user = request.user
        form = ClientForm()
        # form = ClientForm(request.POST, request=request)
        context={}
        # context['form']=ClientForm(request=request)
        
        return render(request, 'bookkeeper_new_client.html', {'form': form})



class loan_application(View):

    def post(self, request, *args, **kwargs):
        forms = LoanApplicationForm(request.POST)
        form = LoanApplicationForm()
        if forms.is_valid():
            success = 'Loan Application created successfuly'
            forms.save()
            return render(request, 'bookkeeper_loan_application.html', {'success':success, 'form': form})
        else:
            error = 'Please fill the form properly'
            print forms.errors
            return render(request, 'bookkeeper_loan_application.html', {'error':error, 'form': form})

    def get(self, request, *args, **kwargs):
        form = LoanApplicationForm()
        return render(request, 'bookkeeper_loan_application.html', {'form': form})  
 
class LoanApproval(View):

    def get(self, request, *args, **kwargs):
        list_of_pending_applications = loanApplication.objects.filter(app_status='Pending')
        return render(request, 'bookkeeper_loan_approval.html', {'applications': list_of_pending_applications})


def approve_loan_application(request, id):
    application = loanApplication.objects.get(app_id=int(id))
    application.app_status = 'Approved'
    application.approval_date = datetime.date.today()
    application.save()
    recent_message = "Loan for {} has been APPROVED.".format(application.client)
    list_of_pending_applications = loanApplication.objects.filter(app_status='Pending')
    return HttpResponseRedirect(reverse('create_loan', kwargs={'id':application.app_id}))

def reject_loan_application(request, id):
    application = loanApplication.objects.get(app_id=int(id))
    application.app_status = 'Denied'
    application.approval_date = datetime.date.today()
    application.save()
    recent_message = "Loan for {} has been DENIED.".format(application.client)
    list_of_pending_applications = loanApplication.objects.filter(app_status='Pending')
    return render(request, 'bookkeeper_loan_approval.html', {'applications': list_of_pending_applications,
        'recent_message': recent_message})


class ClientViewFilter(TemplateView):
    template_name = 'client_list.html'
    
    def get_context_data(self,**kwargs):
        context = super(ClientViewFilter,self).get_context_data(**kwargs)
        name = self.request.GET.get('search', '')
        products = Client.objects.filter(firstname__contains=name)
        context['object_list'] = products
        return context



class ClientViewFilterOne(TemplateView):
    template_name = 'results.html'
    
    def get_context_data(self,**kwargs):
        context = super(ClientViewFilterOne,self).get_context_data(**kwargs)
        name = self.request.GET.get('search', '')
        products = Client.objects.filter(firstname__contains=name)
        context['object_list'] = products
        return context

class CreateLoan(View):
    def get(self, request, *args, **kwargs):
        application = loanApplication.objects.get(app_id=int(self.kwargs.get('id')))
        client = application.client
        print Loan.objects.filter(client=client) # Modify this to only return Boolean (if it has pending loans)
        return render(request, 'create_loan.html', {
            'capital': client.capital,
            'comaker': application.app_comaker
            })

    def post(self, request, *args, **kwargs):

        self.create_loan_info()
        application_id = int(request.get_full_path().split("/")[-1])

        providential = request.POST.get('providential') == 'true'
        emergency =  request.POST.get('emergency') == 'true'
        operator =  request.POST.get('operator') == 'true'
        driver =  request.POST.get('driver') == 'true'
        inline =  request.POST.get('inline') == 'true'
        outline =  request.POST.get('outline') == 'true'
        yescoll =  request.POST.get('yescoll') == 'true'
        nocoll =  request.POST.get('nocoll') == 'true'
        capital =  int(request.POST.get('capital'))
        loan_amount =  int(request.POST.get('loan_amount'))

        interest = 3
        duration = 18

        if providential:
            if operator:
                if inline:
                    if capital >= 20000:
                        if yescoll:
                            if loan_amount <= capital:
                                interest = 1.5
                            else:
                                interest = 3
                            if loan_amount >= 150000:
                                duration = 18
                            else:
                                duration = 12
                        elif nocoll:
                            duration = 12
                            if loan_amount <= capital:
                                interest = 1.5
                            else:
                                interest = 3
                    elif capital < 20000:
                        interest = 3
                        if loan_amount >= 150000:
                            duration = 18
                        else:
                            duration = 12
                elif outline:
                    duration = 12
                    interest = 3
            elif driver:
                duration = 12
                if loan_amount == capital:
                    interest = 1.5
                else:
                    interest = 3
        elif emergency:
            duration = 6
            if capital >= 20000:
                interest = 1.5
            elif capital < 20000:
                interest = 3

        application = loanApplication.objects.get(app_id=application_id)
        type_of_loan = "Providential" if providential else "Emergency"
        loan = Loan(
            client = application.client,
            loan_application = application,
            loan_amount = loan_amount,
            interest_rate = interest,
            loan_duration = duration,
            type_of_loan = type_of_loan,
        )
        loan.save()

        if operator:
            loan.loan_information.add(LoanInformation.objects.get(name="Operator"))
        if driver:
            loan.loan_information.add(LoanInformation.objects.get(name="Driver"))
        if inline:
            loan.loan_information.add(LoanInformation.objects.get(name="Inside Line"))
        if outline:
            loan.loan_information.add(LoanInformation.objects.get(name="Outside Line"))
        

        # print capital
        # print interest
        # print application_id

        return HttpResponse(loan.id)

    def create_loan_info(self):
        LoanInformation.objects.get_or_create(name="Operator")
        LoanInformation.objects.get_or_create(name="Driver")
        LoanInformation.objects.get_or_create(name="Inside Line")
        LoanInformation.objects.get_or_create(name="Outside Line")

class ViewLoanInformation(View):
    def get(self, request, *args, **kwargs):
        loan = Loan.objects.get(id=int(self.kwargs.get('id')))
        name = loan.client
        type_of_loan = loan.type_of_loan
        amount = loan.loan_amount #INCLUDE SUBTRACTION OF INVOICE
        # invoices = Invoice.objects.filter(loan=loan)
        # for invoice in invoices:
        #   amount = amount - invoice.amount
        payment_duration = loan.loan_duration
        interest_rate = loan.interest_rate
        expiration = "{}-{}-{}".format(
            (loan.loan_application.approval_date.month + payment_duration)%12,
            loan.loan_application.approval_date.day,
            loan.loan_application.approval_date.year + (loan.loan_application.approval_date.month + payment_duration)/12
            )
        return render(request, 'loan_created.html', {
            'name': name,
            'type_of_loan': type_of_loan,
            'amount': amount,
            'duration': payment_duration,
            'interest_rate': interest_rate,
            'expiration': expiration
            })

class pay_loan(View):
    def post(self, request, *args, **kwargs):
        forms = PayLoanForm(request.POST)
        form = PayLoanForm()
        if forms.is_valid():
            success = 'Loan Payment Successful'
            forms.save()
            return render(request, 'cashier_loan_pay.html', {'success':success, 'form':form})
        else:
            error = 'Please fill form properly'
            print forms.errors
            return render(request, 'cashier_loan_pay.html', {'error':error, 'form':form})

    def get(self, request, *args, ** kwargs):
        form = PayLoanForm()
        return render(request, 'cashier_loan_pay.html', {'form':form})


def render_receipt(request):
    options = {
    'page-size': 'A5',
    'margin-top': '1in',
    'margin-right': '1in',
    'margin-bottom': '1in',
    'margin-left': '1in',
    'encoding': "UTF-8",
    }

    # content = render_to_string(
    #     'receipt_template.html'
    # )

    # pdf = pdfkit.PDFKit(content, "string", options=options).to_pdf()
    aydi = payLoan.objects.get(pay_id=1)
    projectURL = request.get_host() + '/write_receipt'
    pdf = pdfkit.from_string('receipt_template.html', False, options=options)

    response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Type'] = 'application/pdf'
    # change attachment to inline if you want open file in browser tab instead downloading
    response['Content-Disposition'] = 'inline;filename={}.pdf'.format(aydi.pay_id)

    return response

class write_receipt(View):
    def get(self, request, *args, **kwargs):
        # context = {}
        return render(request, 'receipt_template.html')
