import datetime
import cStringIO as StringIO
import types

# Create your views here.
#views.py
from clients.models import Client, client_capital, Loan, loanApplication, payLoanLedger_in, payLoanLedger_over, MAF, ODF, Restruct
from clients.forms import ClientForm, CollateralForm, CoMakerForm, CapitalForm, LoanApplicationForm, StructLoanApplicationForm, RestructForm, PayLoanForm, PayLoanForm_o, MAFform, ODFform, SavingsForm
from decimal import *
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, redirect, get_list_or_404
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.views.generic import TemplateView
from formtools.preview import FormPreview
from io import BytesIO
from num2words import num2words
from vamps.forms import RegistrationForm

User = get_user_model()


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            )
            user.position=form.cleaned_data['position']
            user.save()
            success = "User is created!"
            return render(request, 'success.html', {'success':success})
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )


@login_required 
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
                    return HttpResponseRedirect(reverse('admin_page'))
                elif user.position == 'Cashier':
                    return HttpResponseRedirect(reverse('cashier_menu'))
                elif user.position == 'Bookkeeper':
                    return HttpResponseRedirect(reverse('book_menu'))
            else:
                
                return render(request, 'login.html', {'error': 'Disabled Account'})
        else:
            
            return render(request, 'login.html', {'error': 'Invalid Credentials'})    
 

class cashier(View):
    """Cashier Home"""
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        loan_id = Loan.objects.filter(loan_status='Outstanding')
        upList = []
        overList = []
        structList = []
        for index in xrange(len(loan_id)):
            if loan_id[index].update == True:
                # context={'notifs':loan_id[index].update}
                upList.append(loan_id[index].client)
                print loan_id[index].update
                # print 'yay'
            else:
                # print 'nay'
                pass

            if loan_id[index].overdue == True:
                overList.append(loan_id[index].client)
            else:
                # print 'nay'
                pass

        prod = Restruct.objects.filter(restruct_status='Outstanding')
        for index in xrange(len(prod)):
            if prod[index].approval_status == False:
                structList.append(prod[index].loan_root)
            else:
                pass
        context = {'upList':upList, 'overList':overList, 'structList':structList}
        if request.user.position == 'Cashier':
            return render(request, "cashier_menu.html", context)
        else:
            return render(request, "restriction.html", context)
        
        
        
class bookkeeper(View):
    """Bookkeeper Home"""

    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        loan_id = Loan.objects.filter(loan_status='Outstanding')
        upList = []
        overList = []
        structList = []
        for index in xrange(len(loan_id)):
            if loan_id[index].update == True:
                # context={'notifs':loan_id[index].update}
                upList.append(loan_id[index].client)
                print loan_id[index].update
                # print 'yay'
            else:
                # print 'nay'
                pass

            if loan_id[index].overdue == True:
                overList.append(loan_id[index].client)
            else:
                # print 'nay'
                pass

        prod = Restruct.objects.filter(restruct_status='Outstanding')
        for index in xrange(len(prod)):
            if prod[index].approval_status == False:
                structList.append(prod[index].loan_root)
            else:
                pass
        context = {'upList':upList, 'overList':overList, 'structList':structList}
        if request.user.position == 'Bookkeeper':
            return render(request, "bookkeeper_menu.html", context)
        else:
            return render(request, "restriction.html", context)



class admin_page(View):
    """Admin Home"""

    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        loan_id = Loan.objects.filter(loan_status='Outstanding')
        upList = []
        overList = []
        structList = []
        for index in xrange(len(loan_id)):
            if loan_id[index].update == True:
                # context={'notifs':loan_id[index].update}
                upList.append(loan_id[index].client)
                print loan_id[index].update
                # print 'yay'
            else:
                # print 'nay'
                pass

            if loan_id[index].overdue == True:
                overList.append(loan_id[index].client)
                # print 'yay'
            else:
                # print 'nay'
                pass

        prod = Restruct.objects.filter(restruct_status='Outstanding')
        for index in xrange(len(prod)):
            if prod[index].approval_status == False:
                structList.append(prod[index].loan_root)
            else:
                pass

        context = {'upList':upList, 'overList':overList, 'structList':structList}
        if request.user.position == 'Admin':
            return render(request, "admin_menu.html", context)
        else:
            return render(request, "restriction.html", context)
        


class UserViewFilter(TemplateView):
    """Opens user search box"""
    template_name = 'user_list.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'user_list.html')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        products = User.objects.filter(last_name__contains=request.POST['search'])
        return render(request, 'user_list.html', {'object_list':products})


class Modify(View):
    """User's modify their credentials here"""

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        logged_user = request.user
        if request.POST['submit'] == 'changemail':
            logged_user = request.user
            curr_email = request.POST.get('curr_email')
            new_email = request.POST.get('new_email')
            logged_email = logged_user.email
            if curr_email != logged_email:
                error = 'Wrong current email'
                return render(request, 'editprofile.html', {'error':error})
            else:
                logged_user.email = new_email
                logged_user.save()
                success = 'Email Change Successfull'
                return render(request, 'editprofile.html', {'success':success})
        
        elif request.POST['submit'] == 'changepass':
            curr_pass = request.POST.get('curr_pass')
            conf_pass = request.POST.get('conf_pass')
            new_pass = request.POST.get('new_pass')
            auth_user = authenticate(username=logged_user, password=curr_pass)
            if new_pass != conf_pass:
                error = 'Password Does Not Match'
                return render(request, 'editprofile.html', {'error':error})
            if auth_user is not None:
                logged_user.set_password(conf_pass)
                logged_user.save()
                success = 'Password Change Successfull'
                return render(request, 'editprofile.html', {'success':success})
            else:
                error = 'Invalid Password'
                return render(request, 'editprofile.html', {'error':error})

        elif request.POST['submit'] =='changeuser':
            curr_usr = request.POST.get('curr_usr')
            new_usr = request.POST.get('new_usr')
            logged_uname = logged_user.username
            if curr_usr != logged_uname:
                error = 'Wrong current username'
                return render(request, 'editprofile.html', {'error':error})
            else:
                logged_user.username = new_usr
                logged_user.save()
                success = 'Username Change Successfull'
                return render(request, 'editprofile.html', {'success':success})

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'editprofile.html', {},)



class add_client(View):
    """Bookkeeper adds new client here"""
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        forms = ClientForm(request.POST)
        form = ClientForm()
        if 'preview' in request.POST:
            form_yr = request.POST.get('birthdate')
            if type(form_yr is types.UnicodeType):
                dummy = datetime.datetime.strptime(form_yr, '%Y-%m-%d').date() #conver unicode to datetime format
                curr_date = datetime.datetime.today().date()
                computed_days = curr_date-dummy #subtract year from birthdate from current year
                computed_age = computed_days/365
                
                if forms.is_valid():
                    forms=ClientForm(initial={
                        'firstname':request.POST.get('firstname'),
                        'middlename':request.POST.get('middlename'),
                        'lastname':request.POST.get('lastname'),
                        'age': computed_age.days,
                        'civil_status':request.POST.get('civil_status'),
                        'phone_number':request.POST.get('phone_number'),
                        'address':request.POST.get('address'),
                        'birthdate':request.POST.get('birthdate'),
                        'educ_attain':request.POST.get('educ_attain'),
                        'occupation':request.POST.get('occupation'),
                        'membership_type':request.POST.get('membership_type'),
                        'client_id_type':request.POST.get('client_id_type'),
                        'client_id_number':request.POST.get('client_id_number'),
                        'beneficiary':request.POST.get('beneficiary')
                        })
                    forms.fields['firstname'].widget.attrs['readonly'] = True
                    forms.fields['middlename'].widget.attrs['readonly'] = True
                    forms.fields['lastname'].widget.attrs['readonly'] = True
                    forms.fields['age'].widget.attrs['readonly'] = True
                    forms.fields['civil_status'].widget.attrs['readonly'] = True
                    forms.fields['phone_number'].widget.attrs['readonly'] = True
                    forms.fields['address'].widget.attrs['readonly'] = True
                    forms.fields['birthdate'].widget.attrs['readonly'] = True
                    forms.fields['educ_attain'].widget.attrs['readonly'] = True
                    forms.fields['occupation'].widget.attrs['readonly'] = True
                    forms.fields['membership_type'].widget.attrs['readonly'] = True
                    forms.fields['client_id_type'].widget.attrs['readonly'] = True
                    forms.fields['client_id_number'].widget.attrs['readonly'] = True
                    forms.fields['beneficiary'].widget.attrs['readonly'] = True
                
                    return render(request, 'preview_new_client.html', {'forms':forms
                    })
                else:
                    print forms.errors
                    messages.error(request, forms.errors)
                    forms.fields['age'].widget.attrs['readonly'] = True
                    return render(request, 'bookkeeper_new_client.html', {'form': forms})
            else:
                print "something was wrong"

        elif 'submit' in request.POST:
            if forms.is_valid():
                forms.save()
                # enable
                messages.success(request, 'Client created successfuly')
                return HttpResponseRedirect('/home/bookkeeper/add-new-client/')
            else:
                error = 'Please fill the form properly'
                return render(request, 'success.html', {'error':error, 'list':forms.errors})


    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        
        form = ClientForm()
        return render(request, 'bookkeeper_new_client.html', {'form': form})      



class ClientViewFilter(TemplateView):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'profile_list.html')


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        products = Client.objects.filter(lastname__contains=request.POST['search'])
        if products:
            return render(request, 'profile_list.html', {'object_list':products})
        else:
            messages.error(request, 'Search returned nothing or Client does not exist')
            return render(request, 'profile_list.html')



class ClientList(View):
    """shows complete list of clients"""
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            products1 = Client.objects.all()
            return render(request, 'clients_list.html', {
                'object_list':products1,
                'count':products1.count(),
                'date':datetime.datetime.today()
                })
        except:
            error = 'There are no clients in the database'
            return render(request, 'success.html', {'error': error})


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        products1 = Client.objects.all()
        products = products1.filter(lastname__startswith=request.POST['search'])
        # products = Client.objects.filter(lastname__startswith=request.POST['search'])
        if products:
            return render(request, 'clients_list.html', {
                'object_list':products,
                'count':products1.count(),
                'date':datetime.datetime.today()
                })
        else:
            messages.error(request, 'Search returned nothing')
            return render(request, 'clients_list.html')


class loan_application(View):
    """Bookkeeper adds loan application here"""

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        forms = LoanApplicationForm(request.POST)
        data = {
            'client': kwargs.get('id'),
            'app_date': request.POST.get('app_date'),
            'app_kind': request.POST.get('app_kind'),
            'app_amount': request.POST.get('app_amount'),
        }
        form = LoanApplicationForm(data)
        if form.is_valid():
            if request.POST['app_kind'] == 'Providential Loan':
                success = 'Loan Application created successfuly'
                form.save()
                # enable
                return render(request, 'success.html', {'success':success})
            else:
                if float(request.POST.get('app_amount')) > 10000.00:
                    error = 'Emergency Loan amount not allowed'
                    return render(request, 'success.html', {'error':error})
                else:
                    success = 'Loan Application created successfuly'
                    form.save()
                    # enable
                    return render(request, 'success.html', {'success':success})
        else:
            error = 'Please fill the form properly'
            return render(request, 'success.html', {'error':error, 'list':forms.errors})

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id)
        cap = client_capital.objects.filter(cap_client=client).last()
        form = LoanApplicationForm(initial={'client': Client.objects.get(cust_number=client_id)})
        form.fields['client'].widget.attrs['readonly'] = True
        form.fields['app_date'].widget.attrs['readonly'] = True
        return render(request, 'bookkeeper_loan_application.html', {
            'form': form,
            'cap':cap,
            'client':client
        })


def approve_loan_application(request, id):
    application = loanApplication.objects.get(app_id=int(id))
    application.app_status = 'Approved'
    application.approval_date = datetime.date.today()
    application.save()
    # enable
    list_of_pending_applications = loanApplication.objects.filter(app_status='Pending')
    return HttpResponseRedirect(reverse('create_loan', kwargs={'id':application.app_id}))


def reject_loan_application(request, id):
    application = loanApplication.objects.get(app_id=id)
    application.app_status = 'Denied'
    application.approval_date = datetime.date.today()
    application.save()
    # enable
    messages.warning(request, "Loan for {} has been DENIED.".format(application.client))
    list_of_pending_applications = loanApplication.objects.filter(app_status='Pending')
    client_id = int(application.client.cust_number)
    return HttpResponseRedirect(reverse('profile', kwargs={'id':client_id}))



class CreateLoan(View):
    """Bookkeeper creates loan here"""

    # @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        coll_form = CollateralForm()
        com_form = CoMakerForm()
        application_id = int(request.get_full_path().split("/")[-1])
        application = loanApplication.objects.get(app_id=int(self.kwargs.get('id')))
        client_cap = client_capital.objects.filter(cap_client=application.client).last()
        client = Client.objects.get(
            lastname=application.client.lastname, 
            firstname=application.client.firstname, 
            middlename=application.client.middlename,
            cust_number=application.client.cust_number)

        try:
            print "here"
            struct = Restruct.objects.filter(loan_root=application.app_id)
            if struct is None:
                pass
            else:
                # ask for payment: restruct fee
                # determine if needs 2 ledgers or 1
                if struct.loan_over_amount == 0.0:
                    create_ledger(
                        0, 
                        struct.loan_in_amount, 
                        "voucher from restruct fee",
                        struct.type_of_loan,
                        struct
                    )
                else:
                    create_ledger(
                        0, 
                        struct.loan_in_amount, 
                        "voucher from restruct fee",
                        struct.type_of_loan,
                        struct
                    )
                    create_ledger_over(
                        0, 
                        struct.loan_in_amount, 
                        "voucher from restruct fee",
                        struct.type_of_loan,
                        struct
                    )
                pass
        except:
            if application.app_kind == 'Providential Loan':
                kind = 'Providential'
                if client.membership_type == 'Operator':
                    # set view/field to Operator
                    # add choices for Inside Line/Outside Line
                    if client_cap.capital >= 20000.00:
                        # check app_amount
                        # all loans auto 1.5 interest
                        if application.app_amount > client_cap.capital:
                            # allowed, must have collateral
                            # set loan_amount
                            over = application.app_amount - client_cap.capital
                            am = client_cap.capital
                            intrs = 3.0
                            cond = True
                            # print 'here oh'
                        else:
                            # app_amount <= client_cap
                            # automatic collateral jeepney unit
                            # ask for collateral details
                            am = application.app_amount
                            intrs = 1.5
                            cond = False
                            # print 'wrong'
                    else:
                        # client_cap < 20000
                        # all loans auto 3.0 interest
                        am = application.app_amount
                        intrs = 3.0
                        if application.app_amount > client_cap.capital:
                            cond = True
                        else:
                            cond = False

                # elif client.membership_type == 'Allied Worker':
                #     # No clue how this goes
                #     kind = 'Providential'
                #     am = application.app_amount

                else:
                    # set view/field to Driver
                    if client_cap.capital >= 20000:
                        # kind = 'Providential'
                        am = application.app_amount
                    #     # check app_amount
                        if application.app_amount > client_cap.capital:
                    #         # allowed, must have co-maker
                    #         # set app_comaker name
                    #         # allowed max app_amount = (capital x 2)
                    #         # set loan_amount
                            intrs = 3.0
                            cond = True
                        else:
                    #         # app_amount < client_cap
                    #         # no app_comaker
                    #         # allowed max app_amount = capital
                    #         # set loan_amount
                            intrs = 1.5
                            cond = False
                    else:
                        intrs = 3.0
                        am = application.app_amount
                    #     # client_cap < 20000
                    #     # check app_amount
                        if application.app_amount > client_cap.capital:
                    #         # allowed, must have co-maker
                    #         # set app_comaker name
                    #         # allowed max app_amount = (capital x 2)
                    #         # set loan_amount
                            cond = True
                        else:
                    #         # app_amount < client_cap
                    #         # no app_comaker needed
                    #         # set loan_amount
                            cond = False
            else:
                # Emergency Loan
                # check for existing approved loan
                kind = 'Emergency'
                all_loan_apps = loanApplication.objects.filter(client=client)
                chosen = len(all_loan_apps) - 2
                # chooses the most recent approved application for providential loan except this loan application
                rec_pay = payLoanLedger_in.objects.filter(client=Loan.objects.filter(client=client)).last()
                # print rec_pay
                cond = False
                if all_loan_apps[chosen].app_kind == 'Providential Loan':
                    if all_loan_apps[chosen].app_status == 'Approved':
                        # check most recent payment
                        # last_pay = rec_pay.trans_date.month - datetime.datetime.now().month
                        if rec_pay:
                            # there is payment
                            # most recent payment must be within two months
                            # reject approval if overdue
                            # kind = 'Emergency'
                            # am = application.app_amount
                            intrs = 3.0
                            messages.success(request, 'Loan Approval recorded. Please finish the loan creation process')
                            # return HttpResponseRedirect('/home/bookkeeper/create-loan/')
                        elif rec_pay == None:
                            messages.error(request, 'Emergency Loan not allowed, previous active loan no initial payment')
                            return HttpResponseRedirect(reverse('profile', kwargs={'id':client.cust_number}))
                        else:
                            # overdue loan
                            # not allowed
                            messages.error(request, 'Emergency Loan not allowed, existing overdue loan')
                            return HttpResponseRedirect(reverse('profile', kwargs={'id':client.cust_number}))
                    else:
                        # all_loan_apps[chosen].app_status == 'Pending' || 'Rejected'
                        messages.error(request, 'Emergency Loan not allowed, {}'.format(all_loan_apps[chosen].app_kind))
                        return HttpResponseRedirect(reverse('profile', kwargs={'id':client.cust_number}))
                        
                else:
                    # no existing Providential Loan
                    # redirect, not allowed
                    messages.error(request, 'Emergency Loan not allowed, no existing Providential Loan')
                    return HttpResponseRedirect(reverse('profile', kwargs={'id':client.cust_number}))

            if application.app_amount >= 150000:
                if kind is 'Providential':
                    mots = 18
                else:
                    mots = 0
            else:
                if kind is 'Providential':
                    mots = 12
                else:
                    mots = 0


            return render(request, 'create_loan_2.html', {
                'client':client,
                'cap': client_cap.capital,
                'type_of_loan': kind,
                'app': application,
                'intrs': intrs,
                'mots': mots,
                'cond': cond,
                'coll': coll_form,
                'com': com_form
            })

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        application_id = int(request.get_full_path().split("/")[-1])
        # application = loanApplication.objects.get(app_id=int(self.kwargs.get('id')))
        application = loanApplication.objects.get(app_id=application_id)
        client_cap = client_capital.objects.filter(cap_client=application.client).last()
        # client = Client.objects.get(lastname=application.client.lastname)
        # add filter for firstname; clients with same lastname is possible

        coll_form = CollateralForm(request.POST)
        com_form = request.POST.get('app_comaker')
        line = request.POST.get('line') # operator line
        ref = request.POST.get('voucher') # voucher number based in user input

        if application.app_kind == 'Providential Loan':
            kind = 'Providential'
            if application.client.membership_type == 'Operator':
                if line == 'Inside Line':
                    if client_cap.capital >= 20000.00:
                        if application.app_amount > client_cap.capital:
                            # over = application.app_amount - client_cap.capital
                            # am = client_cap.capital
                            # mots = 12
                            intrs = 1.5
                            intrs2 = 3.0
                            # must have collateral, must add trigger
                            # max = 150 000 + client_cap
                            # coll_form = CollateralForm(request.POST)
                        else:
                            # application.app_amount <= client_cap
                            # over = 0
                            # am = application.app_amount
                            # mots = 12
                            intrs = 1.5
                            intrs2 = 0
                            # coll_form = False
                    else:
                        # client_cap.capital < 20 000.00
                        # over = 0
                        # am = application.app_amount
                        # mot = 12
                        intrs = 3.0
                        intrs2 = 3.0
                        print "grrr"
                elif line == 'Outside Line':
                    if client_cap.capital >= 20000.00:
                        if application.app_amount > client_cap:
                            # over = application.app_amount - client_cap.capital
                            # am = client_cap.capital
                            # mots = 12
                            intrs = 1.5
                            intrs2 = 3.0
                            # must have collateral
                        else:
                            # application.app_amount <= client_cap
                            # am = application.app_amount
                            # mots = 12
                            intrs = 3.0
                            intrs2 = 0


            elif application.client.membership_type == 'Driver':
                if client_cap.capital >= 20000.00:
                    if application.app_amount > client_cap.capital:
                        # over = application.app_amount - client_cap.capital
                        # am = client_cap.capital
                        intrs = 1.5
                        intrs2 = 3.0
                        # must have co-maker
                    else:
                        # application.app_amount <= client_cap
                        # over = 0
                        # am = application.app_amount
                        intrs = 1.5
                        intrs2 = 0
                else:
                    # client_cap.capital < 20 000.00
                    intrs = 3.0
                    # if application.app_amount > client_cap.capital:
                    #     # ask for co-maker
                    #     over = application.app_amount - client_cap.capital
                    #     am = client_cap.capital
                    #     print 'pasok'
                    # else:
                    #     # application.app_amount <= client_cap
                    #     print 'sa baba'
                    #     am = application.app_amount
                    #     over = 0

            elif application.client.membership_type == 'Allied Worker':
                if client_cap.capital >= 20000.00:
                    if application.app_amount > client_cap.capital:
                        # over = application.app_amount - client_cap.capital
                        # am = client_cap.capital
                        intrs = 1.5
                        intrs2 = 3.0
                    else:
                        # application.app_amount <= client_cap
                        # over = 0
                        # am = application.app_amount
                        intrs = 1.5
                        intrs2 = 0
                else:
                    if application.app_amount > client_cap.capital:
                        intrs = 3.0
                        intrs2 = 3.0
                    else:
                        intrs = 3.0
                        intrs2 = 0
        else:
            # emergency loan
            if ref:
                kind = 'Emergency'
                intrs = 3.0
                intrs2 = 0
            else:
                messages.error(request, 'Please provide the Voucher Number')
                return HttpResponseRedirect(reverse('create_loan', kwargs={'id':kwargs.get('id')}))

        if application.app_amount >= 150000:
            if kind is 'Providential':
                mots = 18
            else:
                mots = request.POST['mot']
        else:
            if kind is 'Providential':
                mots = 12
            else:
                mots = request.POST['mot']

        if application.app_amount > client_cap.capital:
            over = application.app_amount - client_cap.capital
            am = client_cap.capital
            if coll_form.is_valid() and com_form:
                error = 'Non-Fatal Error'
                wrong = ['Please fill out either of the Co-Maker or Collateral', 'Loan cannot have both.'];
                return render(request, 'success.html', {'error':error, 'list':wrong})
            else:
                if coll_form.is_valid():
                    create_loan(application.client, application, am, over, intrs, intrs2, mots, kind)
                    create_ledger(over, am, ref, kind, Loan.objects.get(client=application.client, loan_status="Outstanding"))
                    create_ledger_over(over, am, ref, kind, Loan.objects.get(client=application.client, loan_status="Outstanding"))
                    coll_form.save()
                    # enable
                    print 'success1'
                elif com_form:
                    application.app_comaker = Client.objects.get(cust_number=int(request.POST['app_comaker']))
                    application.save()
                    create_loan(application.client, application, am, over, intrs, intrs2, mots, kind)
                    create_ledger(over, am, ref, kind, Loan.objects.get(client=application.client, loan_status="Outstanding"))
                    create_ledger_over(over, am, ref, kind, Loan.objects.get(client=application.client, loan_status="Outstanding"))
                    # enable
                    print 'success2'

                else:
                    print 'error3'
                    error = 'Please fill out either if the Co-Maker or Collateral'
                    return render(request, 'success.html', {'error':error})

        else:
            if kind is 'Providential':
                if ref:
                    over = 0
                    am = application.app_amount
                    create_loan(application.client, application, am, over, intrs, intrs2, mots, kind)
                    create_ledger(over, am, ref, kind, Loan.objects.get(client=application.client, loan_status="Outstanding"))
                else:
                    messages.error(request, 'Please provide the Voucher Number')
                    return HttpResponseRedirect(reverse('create_loan', kwargs={'id':kwargs.get('id')}))
            else:
                over = 0
                am = application.app_amount
                create_loan(application.client, application, am, over, intrs, intrs2, mots, kind)
                create_ledger(over, am, ref, kind, Loan.objects.get(client=application.client, loan_status="Outstanding", type_of_loan="Emergency"))

        success = 'Loan successfully created'
        return render(request, 'success.html', {'success':success})

# @method_decorator(login_required)
def create_loan(*args):
    loan = Loan(
        client = args[0],
        loan_application = args[1],
        loan_amount = args[2],
        loan_overflow = args[3],
        interest_rate = args[4],
        interest_rate_over = args[5],
        loan_duration = args[6],
        type_of_loan = args[7]
    )

    loan.save()

# @method_decorator(login_required)
def create_ledger(self, request, *args, **kwargs):
    # for creation of loan ledgers within CBU

    print '{} {} {} {}'.format(self, request, args, kwargs)
    ledger_in = payLoanLedger_in(
        client = args[2],
        trans_date = datetime.datetime.now().date(),
        reference = args[0], # voucher number
        debit_loanGranted = request,
        credit_payment = 0,
        int_per_month = 0,
        total_loan_recievable = request,
        loan_pay_type = 'cheque',
        loan_pay_received_by = 'Loan Issuance'
    )

    ledger_in.save()
    # enable

# @method_decorator(login_required)
def create_ledger_over(self, request, *args, **kwargs):
    # for creation of loan ledgers over CBU

    ledger_out = payLoanLedger_over(
        client = args[2],
        trans_date = datetime.datetime.now().date(),
        reference = args[0], # there's somehting here
        debit_loanGranted = self,
        credit_payment = 0,
        int_per_month = 0,
        total_loan_recievable = self,
        loan_pay_type = 'cheque',
        loan_pay_received_by = 'Loan Issuance'
    )
    
    ledger_out.save()
    # enable
    


class ClientProfile(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        client_id = Client.objects.get(cust_number=int(self.kwargs.get('id')))
        client_cap = client_capital.objects.filter(cap_client=client_id).last()

        mafmaf = MAF.objects.filter(maf_client=client_id)
        odfs = ODF.objects.filter(odf_client=client_id)

        loan_app = loanApplication.objects.filter(client=client_id)
        loan_id = Loan.objects.filter(client=client_id, loan_status="Outstanding", type_of_loan="Providential")
        loan_id_2 = Loan.objects.filter(client=client_id, loan_status="Outstanding", type_of_loan="Emergency")
        loan_ledger = payLoanLedger_in.objects.filter(client__type_of_loan="Providential", client=loan_id)
        emer_loan = payLoanLedger_in.objects.filter(client__type_of_loan="Emergency", client=loan_id_2)
        loan_ledger_out = payLoanLedger_over.objects.filter(client=loan_id)
        stru = Restruct.objects.filter(loan_root=loan_app, approval_status=True)
        try:
            if stru.exists():
                print 'go'
                provi_tot = []
                emer_tot = []
                provi_datestart = []
                emer_datestart = []
                provi_xp = []
                emer_xp = []

                for index in xrange(len(loan_id)):
                    provi_tot.append(loan_id[index].loan_amount + loan_id[index].loan_overflow)
                    provi_datestart.append(loan_id[index].loan_application.approval_date)
                    provi_xp.append(compute_dur(loan_id[index].loan_application.approval_date, loan_id[index].loan_duration))
                
                for index in xrange(len(loan_id_2)):
                    emer_tot.append(loan_id_2[index].loan_amount + loan_id_2[index].loan_overflow)
                    emer_datestart.append(loan_id_2[index].loan_application.approval_date)
                    emer_xp.append(compute_dur(loan_id_2[index].loan_application.approval_date, loan_id_2[index].loan_duration))

                return render(request, 'client_profile.html', {
                    'client_cap': client_cap,
                    'loan_app': loan_app,
                    'loan_id': loan_id,
                    'loan_id_2': loan_id_2,
                    'provi_tot':provi_tot,
                    'provi_datestart': provi_datestart,
                    'provi_xp': provi_xp,
                    'emer_tot':emer_tot,
                    'emer_datestart':emer_datestart,
                    'emer_xp': emer_xp,
                    'loan_ledger': loan_ledger,
                    'emer_loan': emer_loan,
                    'loan_ledger_out':loan_ledger_out,
                    'mafmaf': mafmaf,
                    'odfs': odfs,
                    'cust_number': client_id.cust_number,
                    'client_id': client_id,
                    'struct':stru
                })
            else:
                print "else"
                provi_tot = []
                emer_tot = []
                provi_datestart = []
                emer_datestart = []
                provi_xp = []
                emer_xp = []

                for index in xrange(len(loan_id)):
                    provi_tot.append(loan_id[index].loan_amount + loan_id[index].loan_overflow)
                    provi_datestart.append(loan_id[index].loan_application.approval_date)
                    provi_xp.append(compute_dur(loan_id[index].loan_application.approval_date, loan_id[index].loan_duration))
                
                for index in xrange(len(loan_id_2)):
                    emer_tot.append(loan_id_2[index].loan_amount + loan_id_2[index].loan_overflow)
                    emer_datestart.append(loan_id_2[index].loan_application.approval_date)
                    emer_xp.append(compute_dur(loan_id_2[index].loan_application.approval_date, loan_id_2[index].loan_duration))

                return render(request, 'client_profile.html', {
                    'client_cap': client_cap,
                    'loan_app': loan_app,
                    'loan_id': loan_id,
                    'loan_id_2': loan_id_2,
                    'provi_tot':provi_tot,
                    'provi_datestart': provi_datestart,
                    'provi_xp': provi_xp,
                    'emer_tot':emer_tot,
                    'emer_datestart':emer_datestart,
                    'emer_xp': emer_xp,
                    'loan_ledger': loan_ledger,
                    'emer_loan': emer_loan,
                    'loan_ledger_out':loan_ledger_out,
                    'mafmaf': mafmaf,
                    'odfs': odfs,
                    'cust_number': client_id.cust_number,
                    'client_id': client_id,
                    'struct':stru
                })
        except:
            pass
        # try:
        #     # with: everything
        #     # without:
        #     print "try"
        #     if Restruct.objects.get(loan_root=loan_app, approval_status=True):
        #         print "if"
        #         stru = Restruct.objects.get(loan_root=loan_app, approval_status=True)
        #         # struc = stru[0].loan_root
                
        #         provi_tot = []
        #         emer_tot = []
        #         provi_datestart = []
        #         emer_datestart = []
        #         provi_xp = []
        #         emer_xp = []

        #         for index in xrange(len(loan_id)):
        #             provi_tot.append(loan_id[index].loan_amount + loan_id[index].loan_overflow)
        #             provi_datestart.append(loan_id[index].loan_application.approval_date)
        #             provi_xp.append(compute_dur(loan_id[index].loan_application.approval_date, loan_id[index].loan_duration))
                
        #         for index in xrange(len(loan_id_2)):
        #             emer_tot.append(loan_id_2[index].loan_amount + loan_id_2[index].loan_overflow)
        #             emer_datestart.append(loan_id_2[index].loan_application.approval_date)
        #             emer_xp.append(compute_dur(loan_id_2[index].loan_application.approval_date, loan_id_2[index].loan_duration))
        #         print "struct: True"
        #         return render(request, 'client_profile.html', {
        #             'client_cap': client_cap,
        #             'loan_app': loan_app,
        #             'loan_id': loan_id,
        #             'loan_id_2': loan_id_2,
        #             'provi_tot':provi_tot,
        #             'provi_datestart': provi_datestart,
        #             'provi_xp': provi_xp,
        #             'emer_tot':emer_tot,
        #             'emer_datestart':emer_datestart,
        #             'emer_xp': emer_xp,
        #             'loan_ledger': loan_ledger,
        #             'emer_loan': emer_loan,
        #             'loan_ledger_out':loan_ledger_out,
        #             'mafmaf': mafmaf,
        #             'odfs': odfs,
        #             'cust_number': client_id.cust_number,
        #             'client_id': client_id,
        #             'struct':stru
        #         })
        #     else:
        #         print "else1"
        #         provi_tot = []
        #         emer_tot = []
        #         provi_datestart = []
        #         emer_datestart = []
        #         provi_xp = []
        #         emer_xp = []
        #         for index in xrange(len(loan_id)):
        #             provi_tot.append(loan_id[index].loan_amount + loan_id[index].loan_overflow)
        #             provi_datestart.append(loan_id[index].loan_application.approval_date)
        #             provi_xp.append(compute_dur(loan_id[index].loan_application.approval_date, loan_id[index].loan_duration))
                
        #         for index in xrange(len(loan_id_2)):
        #             emer_tot.append(loan_id_2[index].loan_amount + loan_id_2[index].loan_overflow)
        #             emer_datestart.append(loan_id_2[index].loan_application.approval_date)
        #             emer_xp.append(compute_dur(loan_id_2[index].loan_application.approval_date, loan_id_2[index].loan_duration))
        #         print "struct: False"
        #         return render(request, 'client_profile.html', {
        #             'client_cap': client_cap,
        #             'loan_app': loan_app,
        #             'loan_id': loan_id,
        #             'loan_id_2': loan_id_2,
        #             'provi_tot':provi_tot,
        #             'provi_datestart': provi_datestart,
        #             'provi_xp': provi_xp,
        #             'emer_tot':emer_tot,
        #             'emer_datestart':emer_datestart,
        #             'emer_xp': emer_xp,
        #             'loan_ledger': loan_ledger,
        #             'emer_loan': emer_loan,
        #             'loan_ledger_out':loan_ledger_out,
        #             'mafmaf': mafmaf,
        #             'odfs': odfs,
        #             'cust_number': client_id.cust_number,
        #             'client_id': client_id,
        #         })

        # except:
        #     # with: Client
        #     # without: everything
        #     # pwde wala MAF, ODF, client_capital
        #     client_id = Client.objects.get(cust_number=int(self.kwargs.get('id')))
        #     client_cap = client_capital.objects.filter(cap_client=client_id).last()
            
        #     mafmaf = MAF.objects.filter(maf_client=client_id)
        #     odfs = ODF.objects.filter(odf_client=client_id)

        #     print 'except'

        #     return render(request, 'client_profile.html', {
        #         'client_cap': client_cap,
        #         'loan_app': loan_app,
        #         'mafmaf': mafmaf,
        #         'odfs': odfs,
        #         'cust_number': client_id.cust_number,
        #         'client_id': client_id,
        #     })

        # else:
        #     client_id = Client.objects.get(cust_number=int(self.kwargs.get('id')))
        #     client_cap = client_capital.objects.filter(cap_client=client_id).last()
            
        #     mafmaf = MAF.objects.filter(maf_client=client_id)
        #     odfs = ODF.objects.filter(odf_client=client_id)

        #     loan_app = loanApplication.objects.filter(client=client_id)
        #     loan_id = Loan.objects.filter(client=client_id, loan_status="Outstanding", type_of_loan="Providential")
        #     loan_id_2 = Loan.objects.filter(client=client_id, loan_status="Outstanding", type_of_loan="Emergency")
        #     loan_ledger = payLoanLedger_in.objects.filter(client__type_of_loan="Providential", client=loan_id)
        #     emer_loan = payLoanLedger_in.objects.filter(client__type_of_loan="Emergency", client=loan_id_2)
        #     loan_ledger_out = payLoanLedger_over.objects.filter(client=loan_id)

        #     print "else1"
        #     provi_tot = []
        #     emer_tot = []
        #     provi_datestart = []
        #     emer_datestart = []
        #     provi_xp = []
        #     emer_xp = []
        #     for index in xrange(len(loan_id)):
        #         provi_tot.append(loan_id[index].loan_amount + loan_id[index].loan_overflow)
        #         provi_datestart.append(loan_id[index].loan_application.approval_date)
        #         provi_xp.append(compute_dur(loan_id[index].loan_application.approval_date, loan_id[index].loan_duration))
            
        #     for index in xrange(len(loan_id_2)):
        #         emer_tot.append(loan_id_2[index].loan_amount + loan_id_2[index].loan_overflow)
        #         emer_datestart.append(loan_id_2[index].loan_application.approval_date)
        #         emer_xp.append(compute_dur(loan_id_2[index].loan_application.approval_date, loan_id_2[index].loan_duration))
        #     print "struct: False"
        #     return render(request, 'client_profile.html', {
        #         'client_cap': client_cap,
        #         'loan_app': loan_app,
        #         'loan_id': loan_id,
        #         'loan_id_2': loan_id_2,
        #         'provi_tot':provi_tot,
        #         'provi_datestart': provi_datestart,
        #         'provi_xp': provi_xp,
        #         'emer_tot':emer_tot,
        #         'emer_datestart':emer_datestart,
        #         'emer_xp': emer_xp,
        #         'loan_ledger': loan_ledger,
        #         'emer_loan': emer_loan,
        #         'loan_ledger_out':loan_ledger_out,
        #         'mafmaf': mafmaf,
        #         'odfs': odfs,
        #         'cust_number': client_id.cust_number,
        #         'client_id': client_id,
        #     })


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.POST['submit'] == 'changeinfo':
            client_id = Client.objects.get(cust_number=kwargs.get('id'))
            if request.POST['middlename']:
                client_id.middlename = request.POST.get('middlename')
            if request.POST['lastname']:
                client_id.lastname = request.POST.get('lastname')
            if request.POST['civil_status']:
                client_id.civil_status = request.POST.get('civil_status')
            if request.POST['phone_number']:
                client_id.phone_number = request.POST.get('phone_number')
            if request.POST['address']:
                client_id.address = request.POST.get('address')
            if request.POST['birthdate']:
                client_id.birthdate = request.POST.get('birthdate')
            if request.POST['educ_attain']:
                client_id.educ_attain = request.POST.get('educ_attain')
            if request.POST['occupation']:
                client_id.occupation = request.POST.get('occupation')
            if request.POST['membership_type']:
                client_id.membership_type = request.POST.get('membership_type')
            if request.POST['client_id_type']:
                client_id.client_id_type = request.POST.get('client_id_type')
            if request.POST['client_id_number']:
                client_id.client_id_number = request.POST.get('client_id_number')
            if request.POST['beneficiary']:
                client_id.beneficiary = request.POST.get('beneficiary')
            client_id.save()
            success = 'User Information updated!'
            return render(request, 'success.html', {'success':success})
        else:
            error = 'Please fill the details properly'
            return render(request, 'success.html', {'error':error})

# @method_decorator(login_required)
def compute_dur(*args):
    datestart = args[0]
    dur = args[1]
    mot_end = datestart.month + dur

    if mot_end >= 12:
        temp_end_yr = mot_end / 12
            
        f_yr_end = datestart.year+temp_end_yr
        f_date = '{}-{}-{}'.format(f_yr_end, datestart.month, datestart.day)
    else:
        f_date = '{}-{}-{}'.format(datestart.year, datestart.month, datestart.day)

    loan_xp = datetime.datetime.strptime(f_date, '%Y-%m-%d').date()
    return loan_xp



class ViewOldLoanSearch(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'old_loan_ledger_search.html')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        products = Loan.objects.filter(client__lastname__contains=request.POST['search'], loan_status='Paid')
        if products:
            return render(request, 'old_loan_ledger_search.html', {'object_list':products})
        else:
            messages.error(request, 'Search returned nothing. Client and/or Loan may not exist.')
            return render(request, 'old_loan_ledger_search.html')
        


class ViewOldLoan(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        loan_id = kwargs.get('id')
        loan = Loan.objects.get(id=loan_id, loan_status="Paid")
        ledger_in = payLoanLedger_in.objects.filter(client__id=loan_id)
        ledger_out = payLoanLedger_over.objects.filter(client__id=loan_id)
        # print ledger_in

        return render(request, 'old_ledger.html', {'loan':loan, 'ins':ledger_in, 'out':ledger_out})


class PayLoanSearch(TemplateView):
    """Bookkeeper access only. Returns only clients with
    existing Loans"""
    template_name = 'cashier_loanpay_menu.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'cashier_loanpay_menu.html')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        products = Loan.objects.filter(client__lastname__contains=request.POST['search'], loan_status='Outstanding')
        return render(request, 'cashier_loanpay_menu.html', {'object_list':products})

   

class PayLoan(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        forms = PayLoanForm(request.POST)
        form = PayLoanForm_o()
        client_id = int(self.kwargs.get('id'))

        if request.POST['credit_payment'] != "-" and request.POST['reference'] != "-":

            try:
                # go here if model has data
                # must go here because model is pre-populated by createLoan
                ref = payLoanLedger_over.objects.filter(client=client_id).last()
                # print 'try'
                # print ref
                if ref.total_loan_recievable != 0.00:
                    # loan over still not payed
                    # determine to pay overflow(3%) or within CBU(1.5%)
                    print 'if1'
                    print ref.total_loan_recievable

                    if float(request.POST.get('credit_payment')) > float(ref.total_loan_recievable):
                        # payment is greater than outstanding balance in ledger_out
                        # include payment into ledger_in
                        print 'if2'
                        temp = float(request.POST.get('credit_payment')) - float(ref.total_loan_recievable)
                        # for other ledger
                        temp2 = float(request.POST.get('credit_payment')) - float(temp)
                        # for this ledger
                        tot = float(ref.total_loan_recievable) - float(temp2)
                        # print temp
                        # print tot

                        if tot > 0.0:
                            print 'if3'
                            # overflow
                            data = {
                                'client': request.POST.get('client'),
                                'trans_date': request.POST.get('trans_date'),
                                'reference': request.POST.get('reference'),
                                'debit_loanGranted': '',
                                'credit_payment': temp2,
                                'int_per_month': '',   #zero because this must auto update/compute monthly
                                'total_loan_recievable': tot,
                                'loan_pay_type': request.POST.get('loan_pay_type'),
                                'loan_pay_received_by': request.POST.get('loan_pay_received_by')
                            }
                    
                            form = PayLoanForm_o(data)

                            # within CBU
                            ref2 = payLoanLedger_in.objects.filter(client=client_id).last()
                            tot2 = float(ref2.total_loan_recievable) - temp
                            data2 = {
                                'client': request.POST.get('client'),
                                'trans_date': request.POST.get('trans_date'),
                                'reference': request.POST.get('reference'),
                                'debit_loanGranted': '',
                                'credit_payment': temp,
                                'int_per_month': '',   #zero because this must auto update/compute monthly
                                'total_loan_recievable': tot2,
                                'loan_pay_type': request.POST.get('loan_pay_type'),
                                'loan_pay_received_by': request.POST.get('loan_pay_received_by')
                            }

                            forms = PayLoanForm(data2)

                        else:
                            print 'else3'
                            print tot
                            # tot == 0
                            # overflow
                            # tot_x = '({})'.format(tot)
                            data = {
                                'client': request.POST.get('client'),
                                'trans_date': request.POST.get('trans_date'),
                                'reference': request.POST.get('reference'),
                                'debit_loanGranted': '',
                                'credit_payment': temp2,
                                'int_per_month': '',   #zero because this must auto update/compute monthly
                                'total_loan_recievable': tot,
                                'loan_pay_type': request.POST.get('loan_pay_type'),
                                'loan_pay_received_by': request.POST.get('loan_pay_received_by')
                            }
                    
                            form = PayLoanForm_o(data)

                            # within CBU
                            ref2 = payLoanLedger_in.objects.filter(client=client_id).last()
                            tot2 = float(ref2.total_loan_recievable) - temp
                            print tot2
                            data2 = {
                                'client': request.POST.get('client'),
                                'trans_date': request.POST.get('trans_date'),
                                'reference': request.POST.get('reference'),
                                'debit_loanGranted': '',
                                'credit_payment': temp,
                                'int_per_month': '',   #zero because this must auto update/compute monthly
                                'total_loan_recievable': tot2,
                                'loan_pay_type': request.POST.get('loan_pay_type'),
                                'loan_pay_received_by': request.POST.get('loan_pay_received_by')
                            }

                            forms = PayLoanForm(data2)

                    else:
                        # payment is less than or equal to outstanding balance in ledger_out
                        print 'else2'
                        print request.POST.get('credit_payment')
                        tot = float(ref.total_loan_recievable) - float(request.POST.get('credit_payment'))
                        print tot
                        data = {
                            'client': request.POST.get('client'),
                            'trans_date': request.POST.get('trans_date'),
                            'reference': request.POST.get('reference'),
                            'debit_loanGranted': '',
                            'credit_payment': request.POST.get('credit_payment'),
                            'int_per_month': '',   #zero because this must auto update/compute monthly
                            'total_loan_recievable': tot,
                            'loan_pay_type': request.POST.get('loan_pay_type'),
                            'loan_pay_received_by': request.POST.get('loan_pay_received_by')
                        }
                    
                        forms = PayLoanForm_o(data)
                else:
                    print 'else1'
                    # go here if payLoanLedger_over total_loan_recievable == 0

                    ref = payLoanLedger_in.objects.filter(client=client_id).last()
                    if float(request.POST.get('credit_payment')) > float(ref.total_loan_recievable):
                        error = "Overpay"
                        return render(request, 'success.html', {'error':error})
                    else:
                        tot = float(ref.total_loan_recievable) - float(request.POST.get('credit_payment'))
                        if tot != 0.00:
                            data = {
                                'client': request.POST.get('client'),
                                'trans_date': request.POST.get('trans_date'),
                                'reference': request.POST.get('reference'),
                                'debit_loanGranted': '',
                                'credit_payment': request.POST.get('credit_payment'),
                                'int_per_month': '',   #zero because this must auto update/compute monthly
                                'total_loan_recievable': tot,
                                'loan_pay_type': request.POST.get('loan_pay_type'),
                                'loan_pay_received_by': request.POST.get('loan_pay_received_by')
                            }
                            
                        else:
                            # tot == 0
                            data = {
                            'client': request.POST.get('client'),
                            'trans_date': request.POST.get('trans_date'),
                                'reference': request.POST.get('reference'),
                                'debit_loanGranted': '',
                                'credit_payment': request.POST.get('credit_payment'),
                                'int_per_month': '',   #zero because this must auto update/compute monthly
                                'total_loan_recievable': tot,
                                'loan_pay_type': request.POST.get('loan_pay_type'),
                                'loan_pay_received_by': request.POST.get('loan_pay_received_by')
                            }
                            mod = Loan.objects.filter(client=client_id, loan_status="Outstanding").last()
                            mod.loan_status = "Paid"
                            mod.save()
                            mod2 = loanApplication.objects.filter(client=client_id, app_status='Approved').last()
                            mod2.app_status = "Paid"
                            mod2.save()
                        forms = PayLoanForm(data)
                    # print forms.errors

            except:
                # go here if payLoanLedger_over is empty
                # go here if loan_amount is within CBU
                ref = payLoanLedger_in.objects.filter(client=client_id).last()
                print ref
                if float(request.POST.get('credit_payment')) > float(ref.total_loan_recievable):
                    error = "Overpay"
                    return render(request, 'success.html', {'error':error})
                else:
                    tot = float(ref.total_loan_recievable) - float(request.POST.get('credit_payment'))
                    if tot != 0.00:
                        data = {
                            'client': request.POST.get('client'),
                            'trans_date': request.POST.get('trans_date'),
                            'reference': request.POST.get('reference'),
                            'debit_loanGranted': '',
                            'credit_payment': request.POST.get('credit_payment'),
                            'int_per_month': '',   #zero because this must auto update/compute monthly
                            'total_loan_recievable': tot,
                            'loan_pay_type': request.POST.get('loan_pay_type'),
                            'loan_pay_received_by': request.POST.get('loan_pay_received_by')
                        }
                        
                    else:
                        # tot == 0
                        data = {
                        'client': request.POST.get('client'),
                        'trans_date': request.POST.get('trans_date'),
                            'reference': request.POST.get('reference'),
                            'debit_loanGranted': '',
                            'credit_payment': request.POST.get('credit_payment'),
                            'int_per_month': '',   #zero because this must auto update/compute monthly
                            'total_loan_recievable': tot,
                            'loan_pay_type': request.POST.get('loan_pay_type'),
                            'loan_pay_received_by': request.POST.get('loan_pay_received_by')
                        }
                        mod = Loan.objects.filter(client=client_id, loan_status="Outstanding").last()
                        mod.loan_status = "Paid"
                        mod.save()
                        mod2 = loanApplication.objects.filter(client=client_id, app_status='Approved').last()
                        mod2.app_status = "Paid"
                        mod2.save()
                forms = PayLoanForm(data)
                print 'except'

            if forms.is_valid() and form.is_valid():
                # for loans over CBU
                forms.save()
                form.save()
                # enable
                success = 'Loan payment successful and recorded'
                # return render(request, 'receipt_template.html', {'success':success})
                return render(request, 'success.html', {'success':success})
            elif forms.is_valid():
                # for loans within CBU
                forms.save()
                # enable
                success = 'Loan payment successful and recorded'
                # return render(request, 'receipt_template.html', 
                #     {'data':data, 
                #     'client': ref.client,
                #     'user':request.user,
                #     'gen_datetime': datetime.datetime.now(),
                #     'ref':ref.loan_pay_id+1,
                #     'am':num2words(request.POST['credit_payment'])
                #     })
                return render(request, 'success.html', {'success':success})
            else:
                error = 'Please fill the form properly'
                print forms.errors
                print form.errors
                return render(request, 'success.html', {'error':error, 'list': forms.errors, 'list2': form.errors})
        elif request.POST['credit_payment'] == "-":
            error = 'Please fill the form properly'
            wrong = ['Credit/Payment']
            return render(request, 'success.html', {'error':error, 'list':wrong})
        elif request.POST['reference'] == "-":
            error = 'Please fill the form properly'
            wrong = ['OR Number']
            return render(request, 'success.html', {'error':error, 'list':wrong})
        else:
            error = 'Please fill the form properly'
            wrong = ['Credit/Payment', 'OR Number']
            return render(request, 'success.html', {'error':error, 'list':wrong})


    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # can be used to check whether the loan is paid already
        # left here
        loan = Loan.objects.filter(id=int(self.kwargs.get('id'))).last()
        
        if loan.loan_status == 'Outstanding':
            # loan is not yet fully paid
            form = PayLoanForm(initial={'client':loan})
            form.fields['client'].widget.attrs['readonly'] = True

            return render(request, 'cashier_loan_pay.html', {'form': form})  
        elif loan.loan_status == 'Paid':
            # loan is already fully paid
            error = 'Loan is already paid'
            return render(request, 'success.html', {'error':error})
        

class PayCBU(TemplateView):
    template_name = 'cashier_add_cap_menu.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'cashier_add_cap_menu.html')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        products = Client.objects.filter(
            lastname__contains=request.POST['search'], 
            client_status="Active"
        )
        return render(request, 'cashier_add_cap_menu.html', {'object_list':products})
        


class PayCBUform(View):

    def __init__(self):
        self.tot = 0
        self.ref = 0

    def post(self, request, *args, **kwargs):
        form = CapitalForm()
        client_id = int(self.kwargs.get('id'))
        forms = CapitalForm(request.POST)

        try:
            ref = client_capital.objects.get(cap_client=client_id).last() #returns only 1 object
            cred = float(request.POST.get('cap_contrib'))
            ref = float(ref.capital)
            tot = ref + cred

            data = {
                'cap_client': request.POST.get('cap_client'),
                'cap_contrib_date': request.POST.get('cap_contrib_date'),
                'cap_contrib': cred,
                'capital': tot  
            }
            forms = CapitalForm(data)
        except:
            data = {
                'cap_client': request.POST.get('cap_client'),
                'cap_contrib_date': request.POST.get('cap_contrib_date'),
                'cap_contrib': request.POST.get('cap_contrib'),
                'capital': request.POST.get('cap_contrib')
            }
            forms = CapitalForm(data)

        if forms.is_valid():
            forms.save()
            messages.success(request, 'Capital Contribution Recorded')
            return render(request, 'cashier_add_cap.html', {'form':form})
        else:
            raise ValidationError(('%s') % forms.is_bound)

    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id)
        form = CapitalForm(initial={'cap_client': client})
        form.fields['cap_client'].widget.attrs['readonly'] = True
        form.fields['cap_contrib_date'].widget.attrs['readonly'] = True
        return render(request, 'cashier_add_cap.html', {'form':form})

class PayMAF(TemplateView):
    template_name = 'cashier_mafpay_menu.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'cashier_mafpay_menu.html')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        products = Client.objects.filter(
            lastname__contains=request.POST['search'],
            client_status="Active"
        )
        return render(request, 'cashier_mafpay_menu.html', {'object_list':products})



class PayMAFform(View):

    def __init__(self):
        self.tot = 0
        self.ref = 0

    def __int__(self):
        return self.ref

    def post(self, request, *args, ** kwargs):
        form = MAFform()
        client_id = int(request.POST['maf_client'])
        # forms = MAFform(request.POST) #get form data
        # print client_id

        try:   #go here if model already has data
            #fetch last data from total field
            ref = MAF.objects.filter(maf_client__cust_number=client_id).last()   #returns last maf_total
            cred = float(request.POST.get('maf_credit'))   #convert user input(unicode) to float
            ref = float(ref.maf_total)   #convert queryset item to float
            tot = ref + cred   #we use float to accomodate centavos
            # print tot
            data = {
                'maf_client': request.POST.get('maf_client'),
                'maf_contrib_date':request.POST.get('maf_contrib_date'),
                'maf_ref':ref,
                'maf_debit':'',
                'maf_credit':cred,
                'maf_total': tot
            }
            forms = MAFform(data)
            print "try"

        except:   #go here if model is empty
            data = {
                'maf_client':request.POST.get('maf_client'),
                'maf_contrib_date':request.POST.get('maf_contrib_date'),
                'maf_ref': 'forwarded balance',
                'maf_debit': '',
                'maf_credit':request.POST.get('maf_credit'),
                'maf_total': request.POST.get('maf_credit')                
            }
            forms = MAFform(data)
            print "except"

        print ref
        print client_id
        if forms.is_valid():
            forms.save()
            messages.success(request, 'MAF contribution recorded')
            return render(request, 'cashier_mafpay.html', {'form':form})
        else:
            raise ValidationError(('%s') % forms.is_bound)

    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id)
        form = MAFform(initial={'maf_client': client})
        form.fields['maf_client'].widget.attrs['readonly'] = True
        form.fields['maf_contrib_date'].widget.attrs['readonly'] = True
        return render(request, 'cashier_mafpay.html', {'form':form})



class ReleaseMAFsearch(TemplateView):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'cashier_mafrelease_search.html')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        client = Client.objects.filter(
            lastname__contains=request.POST['search'],
            client_status="Active"
            )
        products = []
        
        if client:
            for index in xrange(len(client)):
                mafs = MAF.objects.filter(maf_client=client[index]).last()
                products.append(mafs)
            return render(request, 'cashier_mafrelease_search.html', {'object_list':products})
        else:
            messages.error(request, 'Search returned nothing. Client does not exist or MAF contributions does not exist')
            return render(request, 'cashier_mafrelease_search.html')




class ReleaseMAFform(View):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id)
        fund = MAF.objects.filter(maf_client__cust_number=client_id)
        return render(request, 'cashier_mafrelease.html', {'object_list':fund, 'client':client})


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = MAFform()
        client_id = int(kwargs.get('id'))
        client = Client.objects.get(cust_number=client_id)
        fund = MAF.objects.filter(maf_client__cust_number=client_id, maf_client__client_status="Active").last()

        client.client_status = "Inactive"
        # enable

        data = {
            'maf_client':client_id,
            'maf_contrib_date':datetime.datetime.today().date(),
            'maf_ref': 'MAF release',
            'maf_debit': fund.maf_total,
            'maf_credit': '',
            'maf_total': 0.00
        }

        form = MAFform(data)
        
        if form.is_valid():
            client.save()
            form.save()
            # enable
            # call func to subtract all MAFs
            ReleaseMAFall(client)
            messages.success(request, 'MAF release recorded')
            return HttpResponseRedirect(reverse('release_maf', kwargs={'id':kwargs.get('id')}))
        else:
            error = 'Fatal Error'
            return render(request, 'success.html', {'error':error, 'list':form.errors, 'list2':form})


def ReleaseMAFall(arg):
    """Subtracts Php100.00 from all members with MAF contribution
    if 0.00 or MAF DoesNotExist: pass"""
    clients = Client.objects.filter(client_status="Active")
    
    for index in xrange(len(clients)):
        mafs = MAF.objects.filter(maf_client=clients[index]).last()
        if mafs is None or mafs == 0.00:
            pass
        else:
            data = {
                'maf_client':clients,
                'maf_contrib_date':datetime.datetime.today().date(),
                'maf_ref': 'MAF release for {}'.format(arg),
                'maf_debit': 100.00,
                'maf_credit': '',
                'maf_total': (float(mafs.maf_total)-float(100.00))
            }
            forms = MAFform(data)
        if forms.is_valid():
            forms.save()
            # enable
            print "success"
        else:
            print "error"
            print forms.errors


class PayODFsearch(TemplateView):
    template_name = 'cashier_odfpay_search.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'cashier_odfpay_search.html')


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        products = Client.objects.filter(
            lastname__contains=request.POST['search'],
            client_status="Active"
        )
        # products = ODF.objects.filter(odf_client=client)
        if products:
            return render(request, 'cashier_odfpay_search.html', {'object_list':products})
        else:
            messages.error(request, 'Search returned nothing or client does not exist')
            return render(request, 'cashier_odfpay_search.html')
    


class PayODFform(View):
    def post(self, request, *args, ** kwargs):
        form = ODFform()
        client_id = int(request.POST['odf_client'])
        # forms = ODFform(request.POST) #get form data

        try:   #go here if model already has data
            #fetch last data from total field
            ref = ODF.objects.filter(odf_client=client_id).last()   #returns last odf_total
            cred = float(request.POST.get('odf_credit'))   #convert user input(unicode) to float
            ref = float(ref.odf_total)   #convert queryset item to float
            tot = ref + cred   #we use float to accomodate centavos
            print tot
            data = {
                'odf_client': request.POST.get('odf_client'),
                'odf_contrib_date':request.POST.get('odf_contrib_date'),
                'odf_ref':'deposit',
                'odf_debit':'',
                'odf_credit':cred,
                'odf_total': tot
                }
            forms = ODFform(data)
        except:   #go here if model is empty
            data = {
            'odf_client':request.POST.get('odf_client'),
            'odf_contrib_date':request.POST.get('odf_contrib_date'),
            'odf_ref': 'forwarded balance',
            'odf_debit': '',
            'odf_credit':request.POST.get('odf_credit'),
            'odf_total': request.POST.get('odf_credit')
            }
            forms = ODFform(data)
        print ref
        if request.POST['odf_credit'] != "" or request.POST['odf_credit'] != '-':
            print "error"
            if forms.is_valid():
                # forms.save()
                messages.success(request, 'ODF contribution recorded')
                return render(request, 'cashier_odfpay.html', {'form':form})
            else:
                error = 'Please fill the form properly'
                return render(request, 'success.html', {'error':error, 'list':forms.errors})
        else:
            error = 'Please fill the form properly'
            wrong = ['odf_credit']
            return render(request, 'success.html', {'error':error, 'list':wrong})

    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id, client_status="Active")
        form = ODFform(initial={'odf_client': client})
        form.fields['odf_client'].widget.attrs['readonly'] = True
        form.fields['odf_contrib_date'].widget.attrs['readonly'] = True
        return render(request, 'cashier_odfpay.html', {'form':form, 'Client':client})


class ReleaseODFSearch(TemplateView):
    """Searches only clients with ODF != 0.00"""
    template_name = 'cashier_odf_release.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'cashier_odfrelease_search.html')

    def post(self, request, *args, **kwargs):
        client = Client.objects.filter(
            lastname__contains=request.POST['search'],
            client_status="Active"
            )
        products = ODF.objects.filter(odf_client=client).last()
        if products:
            if products.odf_total != 0.00:
                return render(request, 'cashier_odfrelease_search.html', {'object_list':products})
            else:
                messages.error(request, 'Client have depleted ODF')
                return render(request, 'cashier_odfrelease_search.html', {'object_list':products})
        else:
            messages.error(request, 'Search returned nothing. Client does not exist or ODF contributions does not exist')
            return render(request, 'cashier_odfrelease_search.html')


class ReleaseODFForm(View):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id, client_status='Active')
        form = ODFform(initial={'odf_client':client, 'odf_ref':'Withdrawal'})
        form.fields['odf_client'].widget.attrs['readonly'] = True
        form.fields['odf_contrib_date'].widget.attrs['readonly'] = True
        return render(request, 'cashier_odf_release.html', {'form':form})

    def post(self, request, *args, **kwargs):
        client_id = int(self.kwargs.get('id'))
        client = Client.objects.get(cust_number=client_id, client_status='Active')
        # form = ODFform(initial={'odf_client':client})
        forms = ODFform(request.POST)

        try:
            ref = ODF.objects.filter(odf_client=client).last()   #returns last odf_total
            print 'ref:{}'.format(ref)
            print forms.errors
            deb = float(request.POST['odf_debit'])   #convert user input(unicode) to float
            print 'deb:{}'.format(deb)
            ref = float(ref.odf_total)   #convert queryset item to float
            print 'ref:{}'.format(ref)
            tot = ref - deb   #we use float to accomodate centavos
            print 'tot:{}'.format(tot)
            data = {
                'odf_client': request.POST.get('odf_client'),
                'odf_contrib_date':request.POST.get('odf_contrib_date'),
                'odf_ref':'release',
                'odf_debit':request.POST.get('odf_debit'),
                'odf_credit':'',
                'odf_total': tot
                }
            forms = ODFform(data)            
        except:
            print 'except'
            # print forms.errors
            error = 'Please fill the form properly'
            return render(request, 'success.html', {'error':error, 'list':forms})

        if forms.is_valid():
            forms.save()
            success = 'ODF release recorded'
            return render(request, 'success.html', {'success':success})
        else:
            error = 'Please fill the form properly'
            return render(request, 'success.html', {'error':error, 'list':forms.errors})



class SavingsAddSearch(TemplateView):
    """Cashier/Admin access only. For creating/adding savings"""

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'cashier_savingsSearch.html')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        products = Client.objects.filter(
            lastname__contains=request.POST['search'],
            client_status="Active"
        )
        return render(request, 'cashier_savingsSearch.html', {'object_list':products})



class SavingsAdd(View):
    
    
    def post(self, request, *args, **kwargs):
        form = SavingsForm()
        client_id = int(request.POST['savings_client'])

        try:
            ref = Savings.objects.filter(savings_client__cust_number=client_id).last()
            cred = float(request.POST.get('maf_credit'))
            ref = float(request.savings_total)
            tot = ref + cred

            data = {
                'savings_client': request.POST.get('savings_client'),
                'savings_contrib_date': request.POST.get('savings_contrib_date'),
                'savings_ref': ref,
                'savings_debit': '',
                'savings_credit': cred,
                'savings_total': tot
            }
            forms = SavingsForm(data)

        except:
            data = {
                'savings_client': request.POST.get('savings_client'),
                'savings_contrib_date': request.POST.get('savings_contrib_date'),
                'savings_ref': ref,
                'savings_debit': '',
                'savings_credit': cred,
                'savings_total': tot
            }
            forms = SavingsForm(data)

        if forms.is_valid():
            forms.save()
            messages.success(request, 'Savings contribution saved')
            return render(request, 'cashier_savingsAdd.html', {'form':form})
        else:
            raise ValidationError(('%s') % forms.is_bound())


    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id)
        form = SavingsForm(initial={'savings_client': client})
        form.fields['savings_client'].widget.attrs['readonly'] = True
        form.fields['savings_contrib_date'].widget.attrs['readonly'] = True
        return render(request, 'cashier_savingsAdd.html', {'form':form})



class PayStructFeeSearch(TemplateView):
    """Cashier/Admin access only. Returns loan_apps and restructs that are pending"""

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'cashier_paystructfee_search.html')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        products = Restruct.objects.filter(loan_root__client__lastname__contains=request.POST['search'], approval_status=False)
        if products:
            return render(request, 'cashier_paystructfee_search.html', {'object_list':products})
        else:
            messages.error(request, 'Search returned nothing. Client does not exist or Restructure object does not exist')
            return render(request, 'cashier_paystructfee_search.html')



class PayStructFee(View):
    """Cashier/Admin access only. Returns restruct_id"""

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        struct_id = kwargs.get('id')
        struct = Restruct.objects.get(id=struct_id, approval_status=False)
        # we get only one because User already selected from the search menu
        return render(request, "cashier_paystructfee.html", {'objects':struct})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        struct_id = kwargs.get('id')
        struct = Restruct.objects.get(id=struct_id, approval_status=False)

        struct.restruct_fee = request.POST['fee']
        struct.approval_status = True
        struct.save()
        success = "Payment Successful"
        return render(request, 'success.html', {'success':success})


def fetch_resources(uri, rel):
        path = join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
        return path

# @method_decorator(login_required)
# def checkcheck(request):
#     loan_id = Loan.objects.filter(loan_status="Outstanding") #queryset of all outstanding loans
#     for index in xrange(len(loan_id)):
#         loanApp_id = loan_id[index].loan_application.approval_date
#         loanDur = loan_id[index].loan_duration
#         # print loanApp_id
#         xp = compute_dur(loanApp_id, loanDur)
#         # print xp
#         if datetime.datetime.today().date() <= xp and loanApp_id != datetime.datetime.today().date():
#             if datetime.datetime.today().date().day == loanApp_id.day:
#                 print "update"
#                 loan_id[index].update = True
#                 loan_id[index].save()
#             else:
#                 print "no update"
#         elif datetime.datetime.today().date() <= xp and loanApp_id == datetime.datetime.today().date():
#             print "applied just today"
#         else:
#             loan_id[index].loan_status = 'Overdue'
#             print "overdue"
#     return HttpResponseRedirect(reverse('admin_page'))

# def dailyBackUp(request):
#     # edit path
#     with open('C:\\Users\\yaranon family\\Desktop\\sample.bak', 'w') as f:
#         call_command('dumpdata', indent=3, exclude=['contenttypes', 'auth'], use_natural_foreign_keys=True, stdout=f)
#     return HttpResponseRedirect(reverse('admin_page'))


def update(request, id):
    # may be erroneous
    # for re-test
    loan_id = Loan.objects.get(id=int(id))
    cl = Client.objects.get(cust_number=loan_id.client.cust_number)
    client_cap = client_capital.objects.filter(cap_client=cl).last()
    
    if loan_id.update == True:
        
        try:
            
            ref = payLoanLedger_over.objects.filter(client=loan_id).last()
            ref2 = payLoanLedger_in.objects.filter(client=loan_id).last()
            print client_cap.capital

            if client_cap.capital >= 20000.00:
                intrs = int(ref.total_loan_recievable) * 0.03
                tot = int(ref.total_loan_recievable) + intrs
                intrs2 = int(ref2.total_loan_recievable) * 0.015
                tot2 = int(ref2.total_loan_recievable) + intrs2
                print 'one'
            else:
                intrs = int(ref.total_loan_recievable) * 0.03
                tot = int(ref.total_loan_recievable) + intrs
                intrs2 = int(ref2.total_loan_recievable) * 0.03
                tot2 = int(ref2.total_loan_recievable) + intrs
                print 'not one'

            data1 = payLoanLedger_over(
                client = ref.client,
                trans_date = datetime.datetime.today().date(),
                reference = 'Interest',
                debit_loanGranted = 0,
                credit_payment = 0,
                int_per_month =  intrs,
                total_loan_recievable = tot,
                loan_pay_type = 'cash',
                loan_pay_received_by = 'Bookkeeper'
            )
            data1.save()
            # enable
            
            data2 = payLoanLedger_in(
                client = ref2.client,
                trans_date = datetime.datetime.today().date(),
                reference = 'Interest',
                debit_loanGranted = 0,
                credit_payment = 0,
                int_per_month = intrs2,
                total_loan_recievable = tot2,
                loan_pay_type = 'cash',
                loan_pay_received_by = 'Bookkeeper'
            )
            data2.save()
            loan_id.update = False
            loan_id.save()
            # enable

        except:
            
            ref2 = payLoanLedger_in.objects.filter(client=loan_id).last()
            if client_cap >= 20000.00:
                intrs2 = int(ref2.total_loan_recievable) * 0.015
                tot2 = int(ref2.total_loan_recievable) + intrs2
            else:
                intrs2 = int(ref2.total_loan_recievable) * 0.03
                tot2 = int(ref2.total_loan_recievable) + intrs2
            
            data = payLoanLedger_in(
                client = ref2.client,
                trans_date = datetime.datetime.today().date(),
                reference = 'Interest',
                debit_loanGranted = 0,
                credit_payment = 0,
                int_per_month = intrs2,
                total_loan_recievable = tot2,
                loan_pay_type = 'cash',
                loan_pay_received_by = 'Bookkeeper'
                )
            
            data.save()
            loan_id.update = False
            loan_id.save()
            # enable
    else:
        messages.warning(request, 'Update not scheduled')
    
    return HttpResponseRedirect(reverse('profile', kwargs={'id':loan_id.client.cust_number}))


def restruct(request,id):
    loan_id = Loan.objects.get(id=int(id), overdue=True)
    try:
        loan_in = loan_id.interest_rate
        loan_over = loan_id.interest_rate_over

        if loan_in == 1.5:
            if loan_over == 3.0:
                # 1.5 x 3.0
                # existing loan is above client_cap and client_cap > 20 000
                loan_ledger_in = payLoanLedger_in.objects.filter(client=loan_id).last()
                loan_ledger_out = payLoanLedger_over.objects.filter(client=loan_id).last()
                tot = float(loan_ledger_out.total_loan_recievable) + float(loan_ledger_in.total_loan_recievable)
                data1 = {
                    'client': loan_id.client.cust_number,
                    'app_date': datetime.datetime.today().date(),
                    'app_kind': 'Providential Loan',
                    'app_amount': tot,
                    'restruct': 'True'
                }
                form1 = StructLoanApplicationForm(data1)
                print data1
                if form1.is_valid():
                    form1.save()
                    print "saved"
                else:
                    print form1.errors
                
                info1 = {
                    'loan_root': loan_id.loan_application.app_id,
                    'loan_in_interest': loan_in,
                    'loan_in_amount': loan_ledger_in.total_loan_recievable,
                    'loan_over_interest': loan_over,
                    'loan_over_amount': loan_ledger_out.total_loan_recievable
                }
                struct1 = RestructForm(info1)
                if struct1.is_valid():
                    struct1.save()
                    loan_id.overdue = False
                    loan_id.loan_status = 'Restructured'
                    loan_id.save()
                    print "saved2"
                else:
                    print struct1.errors

            elif loan_over == 0.0:
                # 1.5 x 0.0
                # existing loan is within CBU at the time of application/approval
                loan_ledger_in = payLoanLedger_in.objects.filter(client=loan_id).last()
                # loan_ledger_out = payLoanLedger_over.objects.filter(client=loan_id).last()
                tot = float(loan_ledger_out.total_loan_recievable)
                data1 = {
                    'client': loan_id.client.cust_number,
                    'app_date': datetime.datetime.today().date(),
                    'app_kind': 'Providential Loan',
                    'app_amount': tot,
                    'restruct': 'True'
                }
                form1 = StructLoanApplicationForm(data1)
                if form1.is_valid():
                    form1.save()
                    print "saved"
                else:
                    print form1.errors
                
                info1 = {
                    'loan_root': loan_id.loan_application.app_id,
                    'loan_in_interest': loan_in,
                    'loan_in_amount': loan_ledger_in.total_loan_recievable,
                    'loan_over_interest': 0,
                    'loan_over_amount': 0
                }
                struct1 = RestructForm(info1)
                if struct1.is_valid():
                    struct1.save()
                    loan_id.overdue = False
                    loan_id.loan_status = 'Restructured'
                    loan_id.save()
                    print "saved2"
                else:
                    print struct1.errors

            else:
                # does not exist
                print 'no update'
                pass
        
        else:
            # loan_in == 3.0
            if loan_over == 3.0:
                # 3.0 x 3.0
                # existing loan is above client_cap and client_cap < 20 000
                loan_ledger_in = payLoanLedger_in.objects.filter(client=loan_id).last()
                loan_ledger_out = payLoanLedger_over.objects.filter(client=loan_id).last()
                tot = float(loan_ledger_out.total_loan_recievable) + float(loan_ledger_in.total_loan_recievable)
                
                data2 = {
                    'client': loan_id.client.cust_number,
                    'app_date': datetime.datetime.today().date(),
                    'app_kind': 'Providential Loan',
                    'app_amount': tot,
                    'restruct': 'True'
                }
                form2 = StructLoanApplicationForm(data2)
                if form2.is_valid():
                    form2.save()
                    print "saved"
                else:
                    print form2.errors

                struct_fee = (tot * 0.015) + 50.00
                info2 = {
                    'loan_root': loan_id.loan_application.app_id,
                    'loan_in_interest': loan_in,
                    'loan_in_amount': loan_ledger_in.total_loan_recievable,
                    'loan_over_interest': loan_over,
                    'loan_over_amount': loan_ledger_out.total_loan_recievable,
                    'restruct_fee': struct_fee,
                }
                struct2 = RestructForm(info2)
                if struct2.is_valid():
                    struct2.save()
                    loan_id.overdue = False
                    loan_id.loan_status = 'Restructured'
                    loan_id.save()
                    print "saved2"
                else:
                    print struct2.errors

            elif loan_over == 0.0:
                # 3.0 x 0.0
                # existing loan below CBU but client_cap < 20 000
                loan_ledger_in = payLoanLedger_in.objects.filter(client=loan_id).last()
                tot = float(loan_ledger_out.total_loan_recievable)
                data2 = {
                    'client': loan_id.client,
                    'app_date': datetime.datetime.today().date(),
                    'app_kind': loan_id.type_of_loan,
                    'app_amount': loan_in.total_loan_recievable,
                    'restruct': 'True'
                }
                form2 = StructLoanApplicationForm(data2)
                if form2.is_valid():
                    form2.save()
                    print "saved"
                else:
                    print form2.errors

                info2 = {
                    'loan_root': loan_id.loan_application.app_id,
                    'loan_in_interest': loan_in,
                    'loan_in_amount': loan_ledger_in.total_loan_recievable,
                    'loan_over_interest': 0,
                    'loan_over_amount': 0
                }
                struct2 = RestructForm(info2)
                if struct2.is_valid():
                    struct2.save()
                    loan_id.overdue = False
                    loan_id.loan_status = 'Restructured'
                    loan_id.save()
                    print "saved2"
                else:
                    print struct2.errors
            else:
                # does not exist
                print 'no update'
                pass

    except:
        error = 'Fatal Error. Loan could not be restructured.'
        return render(request, 'success.html', {'error': error})

    return HttpResponseRedirect(reverse('profile', kwargs={'id':loan_id.client.cust_number}))