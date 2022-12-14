import datetime
import cStringIO as StringIO
import types

# Create your views here.
#views.py
from clients.models import Client, client_capital, Loan, loanApplication, payLoanLedger_in, payLoanLedger_over, MAF, ODF, Savings, Restruct
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
            print form.errors
            list2 = {"This value must contain only letters, numbers and underscores"}
            error = "Please fill the form properly"
            return render(request, 'success.html', {'error':error, 'list':form.errors, 'list2':list2})
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
                messages.success(request, 'Client created successfully')
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
            products1 = Client.objects.all().order_by('lastname')
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
                        # print "grrr"
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
                    if application.app_amount > client_cap.capital:
                        intrs2 = 3.0
                    #     # ask for co-maker
                    #     over = application.app_amount - client_cap.capital
                    #     am = client_cap.capital
                    #     print 'pasok'
                    else:
                        intrs2 = 0
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
                    create_ledger(over, am, ref, kind, Loan.objects.filter(client=application.client, loan_status = "Outstanding", type_of_loan="Providential").last())
                    create_ledger_over(over, am, ref, kind, Loan.objects.filter(client=application.client, loan_status = "Outstanding", type_of_loan="Providential").last())
                    coll_form.save()
                    # enable
                    print 'success1'
                elif com_form:
                    application.app_comaker = Client.objects.get(cust_number=int(request.POST['app_comaker']))
                    application.save()
                    create_loan(application.client, application, am, over, intrs, intrs2, mots, kind)
                    create_ledger(over, am, ref, kind, Loan.objects.filter(client=application.client, loan_status="Outstanding", type_of_loan="Providential").last())
                    create_ledger_over(over, am, ref, kind, Loan.objects.filter(client=application.client, loan_status="Outstanding", type_of_loan="Providential").last())
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
                    create_ledger(over, am, ref, kind, Loan.objects.filter(client=application.client, loan_status = "Outstanding", type_of_loan="Providential").last())
                else:
                    messages.error(request, 'Please provide the Voucher Number')
                    return HttpResponseRedirect(reverse('create_loan', kwargs={'id':kwargs.get('id')}))
            else:
                over = 0
                am = application.app_amount
                create_loan(application.client, application, am, over, intrs, intrs2, mots, kind)
                create_ledger(over, am, ref, kind, Loan.objects.filter(client=application.client, loan_status="Outstanding", type_of_loan="Emergency").last())

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
        savings = Savings.objects.filter(savings_client=client_id)

        loan_app = loanApplication.objects.filter(client=client_id)
        loan_id = Loan.objects.filter(client=client_id, loan_status="Outstanding", type_of_loan="Providential")
        loan_id_2 = Loan.objects.filter(client=client_id, loan_status="Outstanding", type_of_loan="Emergency")
        loan_ledger = payLoanLedger_in.objects.filter(client__type_of_loan="Providential", client__client=client_id)
        emer_loan = payLoanLedger_in.objects.filter(client__type_of_loan="Emergency", client__client=client_id)
        loan_ledger_out = payLoanLedger_over.objects.filter(client__type_of_loan="Providential", client__client=client_id)
        stru = Restruct.objects.filter(loan_root = loan_app, loan_root__restruct=True, approval_status=True).last()
        try:
            if stru:
                provi_tot = []
                emer_tot = []
                provi_datestart = []
                emer_datestart = []
                provi_xp = []
                emer_xp = []
                provi_ledger = []
                if loan_id and loan_id_2:

                    for index in xrange(len(loan_id)):
                        provi_tot.append(loan_id[index].loan_amount + loan_id[index].loan_overflow)
                        provi_datestart.append(loan_id[index].loan_application.approval_date)
                        provi_xp.append(compute_dur(loan_id[index].loan_application.approval_date, loan_id[index].loan_duration))
                        provi = zip(loan_id, provi_tot, provi_datestart, provi_xp)

                    
                    for index in xrange(len(loan_id_2)):
                        emer_tot.append(loan_id_2[index].loan_amount + loan_id_2[index].loan_overflow)
                        emer_datestart.append(loan_id_2[index].loan_application.approval_date)
                        emer_xp.append(compute_dur(loan_id_2[index].loan_application.approval_date, loan_id_2[index].loan_duration))
                        emer = zip(loan_id_2, emer_tot, emer_datestart, emer_xp)

                    return render(request, 'client_profile.html', {
                        'client_cap': client_cap,
                        'loan_app': loan_app,
                        'loan_id': loan_id,
                        'loan_id_2': loan_id_2,
                        'provi':provi,
                        'emer':emer,
                        'loan_ledger': loan_ledger,
                        'emer_loan': emer_loan,
                        'loan_ledger_out':loan_ledger_out,
                        'mafmaf': mafmaf,
                        'odfs': odfs,
                        'savings': savings,
                        'cust_number': client_id.cust_number,
                        'client_id': client_id,
                        'struct':stru
                    })
                else:
                    if loan_id:
                        for index in xrange(len(loan_id)):
                            provi_tot.append(loan_id[index].loan_amount + loan_id[index].loan_overflow)
                            provi_datestart.append(loan_id[index].loan_application.approval_date)
                            provi_xp.append(compute_dur(loan_id[index].loan_application.approval_date, loan_id[index].loan_duration))
                            provi = zip(loan_id, provi_tot, provi_datestart, provi_xp)
                        return render(request, 'client_profile.html', {
                            'client_cap': client_cap,
                            'loan_app': loan_app,
                            'loan_id': loan_id,
                            'loan_id_2': loan_id_2,
                            'provi':provi,
                            'loan_ledger': loan_ledger,
                            'emer_loan': emer_loan,
                            'loan_ledger_out':loan_ledger_out,
                            'mafmaf': mafmaf,
                            'odfs': odfs,
                            'savings': savings,
                            'cust_number': client_id.cust_number,
                            'client_id': client_id,
                            'struct':stru
                        })
                    else:
                        for index in xrange(len(loan_id_2)):
                            emer_tot.append(loan_id_2[index].loan_amount + loan_id_2[index].loan_overflow)
                            emer_datestart.append(loan_id_2[index].loan_application.approval_date)
                            emer_xp.append(compute_dur(loan_id_2[index].loan_application.approval_date, loan_id_2[index].loan_duration))
                            emer = zip(loan_id_2, emer_tot, emer_datestart, emer_xp)
                        return render(request, 'client_profile.html', {
                            'client_cap': client_cap,
                            'loan_app': loan_app,
                            'loan_id': loan_id,
                            'loan_id_2': loan_id_2,
                            'emer':emer,
                            'loan_ledger': loan_ledger,
                            'emer_loan': emer_loan,
                            'loan_ledger_out':loan_ledger_out,
                            'mafmaf': mafmaf,
                            'odfs': odfs,
                            'savings': savings,
                            'cust_number': client_id.cust_number,
                            'client_id': client_id,
                            'struct':stru
                        })
            else:
                print "else"
                print loan_ledger_out
                provi_tot = []
                emer_tot = []
                provi_datestart = []
                emer_datestart = []
                provi_xp = []
                emer_xp = []
                bals = []
                if loan_id and loan_id_2:

                    for index in xrange(len(loan_id)):
                        provi_tot.append(loan_id[index].loan_amount + loan_id[index].loan_overflow)
                        provi_datestart.append(loan_id[index].loan_application.approval_date)
                        provi_xp.append(compute_dur(loan_id[index].loan_application.approval_date, loan_id[index].loan_duration))
                        provi = zip(loan_id, provi_tot, provi_datestart, provi_xp)

                
                    for index in xrange(len(loan_id_2)):
                        emer_tot.append(loan_id_2[index].loan_amount + loan_id_2[index].loan_overflow)
                        emer_datestart.append(loan_id_2[index].loan_application.approval_date)
                        emer_xp.append(compute_dur(loan_id_2[index].loan_application.approval_date, loan_id_2[index].loan_duration))
                        emer = zip(loan_id_2, emer_tot, emer_datestart, emer_xp)

                    return render(request, 'client_profile.html', {
                        'client_cap': client_cap,
                        'loan_app': loan_app,
                        'loan_id': loan_id,
                        'loan_id_2': loan_id_2,
                        'provi':provi,
                        'emer':emer,
                        'loan_ledger': loan_ledger,
                        'emer_loan': emer_loan,
                        'loan_ledger_out':loan_ledger_out,
                        'mafmaf': mafmaf,
                        'odfs': odfs,
                        'savings': savings,
                        'cust_number': client_id.cust_number,
                        'client_id': client_id,
                    })
                else:
                    if loan_id:
                        for index in xrange(len(loan_id)):
                            provi_tot.append(loan_id[index].loan_amount + loan_id[index].loan_overflow)
                            provi_datestart.append(loan_id[index].loan_application.approval_date)
                            provi_xp.append(compute_dur(loan_id[index].loan_application.approval_date, loan_id[index].loan_duration))
                            provi = zip(loan_id, provi_tot, provi_datestart, provi_xp)
                        return render(request, 'client_profile.html', {
                            'client_cap': client_cap,
                            'loan_app': loan_app,
                            'loan_id': loan_id,
                            'loan_id_2': loan_id_2,
                            'provi':provi,
                            'loan_ledger': loan_ledger,
                            'emer_loan': emer_loan,
                            'loan_ledger_out':loan_ledger_out,
                            'mafmaf': mafmaf,
                            'odfs': odfs,
                            'savings': savings,
                            'cust_number': client_id.cust_number,
                            'client_id': client_id,
                        })
                    else:
                        for index in xrange(len(loan_id_2)):
                            emer_tot.append(loan_id_2[index].loan_amount + loan_id_2[index].loan_overflow)
                            emer_datestart.append(loan_id_2[index].loan_application.approval_date)
                            emer_xp.append(compute_dur(loan_id_2[index].loan_application.approval_date, loan_id_2[index].loan_duration))
                            emer = zip(loan_id_2, emer_tot, emer_datestart, emer_xp)
                        return render(request, 'client_profile.html', {
                            'client_cap': client_cap,
                            'loan_app': loan_app,
                            'loan_id': loan_id,
                            'loan_id_2': loan_id_2,
                            'emer':emer,
                            'loan_ledger': loan_ledger,
                            'emer_loan': emer_loan,
                            'loan_ledger_out':loan_ledger_out,
                            'mafmaf': mafmaf,
                            'odfs': odfs,
                            'savings': savings,
                            'cust_number': client_id.cust_number,
                            'client_id': client_id,
                        })
        except:
            raise Http404
            # pass


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
    dd = 0
    # mot_end = datestart.month + dur
    if datestart.day == 31:
        dd += 30
    else:
        dd += datestart.day

    if dur == 12:
        f_yr_end = datestart.year+1
        f_date = '{}-{}-{}'.format(f_yr_end, datestart.month, dd)
        pass
    elif dur > 12:
        temp_end_yr = dur/12
        mot_end = dur%12
        f_yr_end = datestart.year+temp_end_yr
        f_date = '{}-{}-{}'.format(f_yr_end, datestart.month, dd)
        pass
    else:
        mot_end = datestart.month + dur
        if mot_end > 12:
            temp_end_yr = mot_end/12
            temp_end_mot = mot_end%12
            f_yr_end = datestart.year+temp_end_yr
            f_date = '{}-{}-{}'.format(f_yr_end, temp_end_mot, dd)
            pass
        elif mot_end == 12:
            f_date = '{}-{}-{}'.format(datestart.year+1, datestart.month, dd)
            pass
        else:
            f_date = '{}-{}-{}'.format(datestart.year, mot_end, dd)
            pass


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
    """Returns only clients with
    existing Loans"""
    template_name = 'cashier_loanpay_menu.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'cashier_loanpay_menu.html')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        bals = []
        products = Loan.objects.filter(client__lastname__contains=request.POST['search'], loan_status='Outstanding')
        for index in xrange(len(products)):
            temp_bal_in = payLoanLedger_in.objects.filter(client=products[index]).last()
            temp_bal_out = payLoanLedger_over.objects.filter(client=products[index]).last()
            if temp_bal_out:
                temp_tot = temp_bal_in.total_loan_recievable + temp_bal_out.total_loan_recievable
                bals.append(temp_tot)
            else:
                bals.append(temp_bal_in.total_loan_recievable)
            
        balance = zip(products, bals)
        return render(request, 'cashier_loanpay_menu.html', {'object_list':products, 'balance':balance})

   

class PayLoan(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = PayLoanForm()
        form2 = PayLoanForm_o()
        client_id = int(self.kwargs.get('id'))
        user_input = request.POST['credit_payment']
        # print kwargs

        if request.POST['credit_payment'] != "" or request.POST['reference'] != "":

            try:
                # go here if model has data
                # must go here because model is pre-populated by createLoan
                ref_out = payLoanLedger_over.objects.filter(client=client_id).last()
                ref_in = payLoanLedger_in.objects.filter(client=client_id).last()
                ref_tot = float(ref_out.total_loan_recievable)+float(ref_in.total_loan_recievable)
                if user_input:
                    if float(request.POST.get('credit_payment')) > ref_tot:
                        error = "Pay amount exceeding remaining loan balance"
                        list2 = ['remaining balance:', ref_tot]
                        return render(request, 'success.html', {'error':error, 'list':list2})
                    else:
                        if float(ref_tot) != 0.00:
                            # loan over still not payed
                            # determine to pay overflow(3%) or within CBU(1.5%)
                            if float(ref_out.total_loan_recievable) != 0.00 and float(ref_in.total_loan_recievable) != 0.00:
                                # false-false if overflow is not yet payed
                                # true-false if overflow is payed, therefore pay only in
                                if float(user_input) > float(ref_out.total_loan_recievable):
                                    # payment is greater than balance in loan_ledger_out
                                    temp = float(user_input) - float(ref_out.total_loan_recievable)
                                    tot = float(ref_in.total_loan_recievable) - temp

                                    data2 = {
                                        'client': request.POST.get('client'),
                                        'trans_date': request.POST.get('trans_date'),
                                        'reference': request.POST.get('reference'),
                                        'debit_loanGranted': '',
                                        'credit_payment': ref_out.total_loan_recievable,
                                        'int_per_month': '',   #zero because this must auto update/compute monthly
                                        'total_loan_recievable': 0.00,
                                        'loan_pay_type': request.POST.get('loan_pay_type'),
                                        'loan_pay_received_by': request.user.position
                                    }

                                    if tot >= float(ref_in.total_loan_recievable):
                                        data = {
                                            'client': request.POST.get('client'),
                                            'trans_date': request.POST.get('trans_date'),
                                            'reference': request.POST.get('reference'),
                                            'debit_loanGranted': '',
                                            'credit_payment': ref_in.total_loan_recievable,
                                            'int_per_month': '',   #zero because this must auto update/compute monthly
                                            'total_loan_recievable': 0.00,
                                            'loan_pay_type': request.POST.get('loan_pay_type'),
                                            'loan_pay_received_by': request.user.position
                                        }
                                        loan_id = Loan.objects.get(id=client_id)
                                        loan_id.loan_status = 'Paid'
                                        loan_id.save()
                                    else:
                                        data = {
                                            'client': request.POST.get('client'),
                                            'trans_date': request.POST.get('trans_date'),
                                            'reference': request.POST.get('reference'),
                                            'debit_loanGranted': '',
                                            'credit_payment': temp,
                                            'int_per_month': '',   #zero because this must auto update/compute monthly
                                            'total_loan_recievable': tot,
                                            'loan_pay_type': request.POST.get('loan_pay_type'),
                                            'loan_pay_received_by': request.user.position
                                        }
                                    
                                    form = PayLoanForm(data)
                                    form2 = PayLoanForm_o(data2)
                                else:
                                    # credit_payment <= out_total
                                    tot2 = float(ref_out.total_loan_recievable) -  float(request.POST.get('credit_payment'))
                                    data2 = {
                                        'client': request.POST.get('client'),
                                        'trans_date': request.POST.get('trans_date'),
                                        'reference': request.POST.get('reference'),
                                        'debit_loanGranted': '',
                                        'credit_payment': request.POST.get('credit_payment'),
                                        'int_per_month': '',   #zero because this must auto update/compute monthly
                                        'total_loan_recievable': tot2,
                                        'loan_pay_type': request.POST.get('loan_pay_type'),
                                        'loan_pay_received_by': request.user.position
                                    }
                                    form2 = PayLoanForm_o(data2)

                            else:
                                # ledger_out is done, pay only ledger_in
                                if float(ref_in.total_loan_recievable) != 0.00:
                                    if float(user_input) > float(ref_in.total_loan_recievable):

                                        temp = float(user_input) - float(ref_in.total_loan_recievable)
                                        tot = float(ref_in.total_loan_recievable) - temp
                                        data = {
                                            'client': request.POST.get('client'),
                                            'trans_date': request.POST.get('trans_date'),
                                            'reference': request.POST.get('reference'),
                                            'debit_loanGranted': '',
                                            'credit_payment': ref_in.total_loan_recievable,
                                            'int_per_month': '',   #zero because this must auto update/compute monthly
                                            'total_loan_recievable': 0.00,
                                            'loan_pay_type': request.POST.get('loan_pay_type'),
                                            'loan_pay_received_by': request.user.position
                                        }
                                        change = {'change':temp}
                                        form = PayLoanForm(data)
                                        if tot == 0.00:
                                            loan_id = Loan.objects.get(id=client_id)
                                            loan_id.loan_status = 'Paid'
                                            loan_id.save()
                                    else:
                                        print 'here'
                                        temp = float(ref_in.total_loan_recievable) - float(request.POST.get('credit_payment'))
                                        data = {
                                            'client': request.POST.get('client'),
                                            'trans_date': request.POST.get('trans_date'),
                                            'reference': request.POST.get('reference'),
                                            'debit_loanGranted': '',
                                            'credit_payment': request.POST.get('credit_payment'),
                                            'int_per_month': '',   #zero because this must auto update/compute monthly
                                            'total_loan_recievable': temp,
                                            'loan_pay_type': request.POST.get('loan_pay_type'),
                                            'loan_pay_received_by': request.user.position
                                        }
                                        form = PayLoanForm(data)
                                        if temp == 0.00:
                                            loan_id = Loan.objects.get(id=client_id)
                                            loan_id.loan_status = 'Paid'
                                            loan_id.save()

                                else:
                                    # loan already paid
                                    pass
                        else:
                        # loan already paid
                            pass
                else:
                    error = 'Please fill form properly'
                    list2 = ['no input amount at Credit']
                    return render(request, 'success.html', {'error':error, 'list':list2})
                        
            except Exception, e:
                # raise e
                # raise Http404
                # pass
                if user_input:
                    ref_in = payLoanLedger_in.objects.filter(client=client_id).last()

                    if float(user_input) > float(ref_in.total_loan_recievable):
                        error = "Pay amount exceeding remaining loan balance"
                        list2 = ['remaining balance: {}'.format(float(ref_in.total_loan_recievable))]
                        return render(request, 'success.html', {'error':error, 'list':list2})
                    else:
                        if float(ref_in.total_loan_recievable) != 0.00:
                            if float(user_input) == float(ref_in.total_loan_recievable):
                                data = {
                                    'client': request.POST.get('client'),
                                    'trans_date': request.POST.get('trans_date'),
                                    'reference': request.POST.get('reference'),
                                    'debit_loanGranted': '',
                                    'credit_payment': request.POST.get('credit_payment'),
                                    'int_per_month':'',
                                    'total_loan_recievable': 0.00,
                                    'loan_pay_type': request.POST.get('loan_pay_type'),
                                    'loan_pay_received_by': request.user.position
                                }
                                form = PayLoanForm(data)
                                loan_id = Loan.objects.get(id=client_id)
                                loan_id.loan_status = 'Paid'
                                loan_id.save()
                            else:
                                # payment is less than the remaining balance
                                tot = float(ref_in.total_loan_recievable) - float(request.POST.get('credit_payment'))
                                data = {
                                    'client':request.POST.get('client'),
                                    'trans_date':request.POST.get('trans_date'),
                                    'reference':request.POST.get('reference'),
                                    'debit_loanGranted': '',
                                    'credit_payment': request.POST.get('credit_payment'),
                                    'int_per_month': '',
                                    'total_loan_recievable': tot,
                                    'loan_pay_type':request.POST.get('loan_pay_type'),
                                    'loan_pay_received_by': request.user.position
                                }
                                form = PayLoanForm(data)
                else:
                    error = 'Please fill form properly'
                    list2 = ['no input amount at Credit']
                    return render(request, 'success.html', {'error':error, 'list':list2})
                
            # else:
            if form.is_valid() and form2.is_valid():
                # for loan payment including 2 ledgers
                form2.save()
                form.save()
                # enable
                success = 'Loan payment successful and recorded'
                print 11
                return render(request, 'receipt_template.html',{
                    'data':data, 
                    'client': ref_out,
                    'user':request.user,
                    'gen_datetime': datetime.datetime.now(),
                    'ref':ref_out.loan_pay_id+1,
                    'am':num2words(request.POST.get('credit_payment'))
                    })
            else:
                if form2.is_valid():
                    # for loans outside CBU
                    form2.save()
                    # enable
                    # success = 'Loan payment successful and recorded'
                    print request.user
                    return render(request, 'receipt_template.html', {
                        'data':data2, 
                        'client': ref_out,
                        'user':request.user,
                        'gen_datetime': datetime.datetime.now(),
                        'ref':ref_out.loan_pay_id+1,
                        'am':num2words(request.POST['credit_payment'])
                        })
                elif form.is_valid():
                    # for loans within CBU
                    form.save()
                    # enable
                    # success = 'Loan payment successful and recorded'
                    print request.user
                    print ref_in.client.loan_status
                    return render(request, 'receipt_template.html', 
                        {'data':data, 
                        'client': ref_in,
                        'user':request.user,
                        'gen_datetime': datetime.datetime.now(),
                        'ref':ref_in.loan_pay_id+1,
                        'am':num2words(request.POST['credit_payment'])
                        })
                else:
                    error = 'Please fill the form properly'
                    print form.errors
                    print form2.errors
                    return render(request, 'success.html', {'error':error, 'list': form.errors, 'list2': form2.errors})

        elif request.POST['credit_payment'] == "":
            error = 'Please fill the form properly'
            wrong = ['Credit/Payment']
            return render(request, 'success.html', {'error':error, 'list':wrong})
        elif request.POST['reference'] == "":
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
            print loan.client
            form = PayLoanForm(initial={'client':loan, 'loan_pay_received_by':request.user.position})
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
        # ref = client_capital.objects.get(cap_client=client_id).last() #returns only 1 object

        try:
            # capital is present
            ref = client_capital.objects.filter(cap_client=client_id).last() #returns only 1 object
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
            # go here to create capital
            data = {
                'cap_client': request.POST.get('cap_client'),
                'cap_contrib_date': request.POST.get('cap_contrib_date'),
                'cap_contrib': request.POST.get('cap_contrib'),
                'capital': request.POST.get('cap_contrib')
            }
            forms = CapitalForm(data)

        if forms.is_valid():
            forms.save()
            success = 'Capital Contribution Recorded'
            return render(request, 'success.html', {'success':success})
        else:
            error = "Please fill the form properly."
            return render(request, 'success.html', {'error':error, 'list':forms.errors})

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
        user_input = request.POST['maf_credit']
        # forms = MAFform(request.POST) #get form data
        # print client_id

        try:   #go here if model already has data
            #fetch last data from total field
            ref = MAF.objects.filter(maf_client__cust_number=client_id).last()   #returns last maf_total
            if user_input:
                cred = float(request.POST.get('maf_credit'))   #convert user input(unicode) to float
                ref = float(ref.maf_total)   #convert queryset item to float
                tot = ref + cred   #we use float to accomodate centavos
                # print tot
                data = {
                    'maf_client': request.POST.get('maf_client'),
                    'maf_contrib_date':request.POST.get('maf_contrib_date'),
                    'maf_ref':'deposit',
                    'maf_debit':'',
                    'maf_credit':cred,
                    'maf_total': tot
                }
                forms = MAFform(data)
            else:
                error ='Please fill the form properly'
                list2 = ['no input value at Credit']
                return render(request, 'success.html', {'error':error, 'list':list2})
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

        if forms.is_valid():
            forms.save()
            success = 'MAF contribution recorded'
            return render(request, 'success.html', {'success':success})
        else:
            error = 'Please fill the form properly'
            return render(request, 'success.html', {'error':error, 'list':forms.errors})

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
        return render(request, 'cashier_mafrelease_search.html', {'object_list':'here'})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        client = Client.objects.filter(
            lastname__contains=request.POST['search'],
            client_status="Active"
            )
        products = []
        client_list = []
        
        if client:
            for index in xrange(len(client)):
                mafs = MAF.objects.filter(maf_client=client[index]).last()
                if mafs != None:
                    products.append(mafs)
                else:
                    client_list.append(client[index])
            # return render(request, 'cashier_mafrelease_search.html', {'object_list':products, 'client_list':client_list})
        else:
            messages.error(request, 'Search returned nothing. Client does not exist or MAF contributions does not exist')
        return render(request, 'cashier_mafrelease_search.html', {'object_list':products, 'client_list':client_list})




class ReleaseMAFtable(TemplateView):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id)
        fund = MAF.objects.filter(maf_client__cust_number=client_id)
        return render(request, 'cashier_mafrelease_tableview.html', {'object_list':fund, 'client':client})



class ReleaseMAF(View):

    def get(self, request, *args, **kwargs):
        client_id = int(kwargs.get('id'))
        client = Client.objects.get(cust_number=client_id)
        date = datetime.datetime.today().date()
        try:
            fund = MAF.objects.filter(maf_client__cust_number=client_id, maf_client__client_status="Active").last()
            return render(request, 'cashier_mafrelease_form.html', {'client':client, 'date':date, 'fund':fund})
        except:
            # fund = MAF.objects.filter(maf_client__cust_number=client_id, maf_client__client_status="Active").last()
            return render(request, 'cashier_mafrelease_form.html', {'client':client, 'date':date})

    def post(self, request, *args, **kwargs):
        client_id = int(kwargs.get('id'))
        curr_client = Client.objects.get(cust_number=client_id)
        clients = Client.objects.filter(client_status="Active")
        date = datetime.datetime.today().date()
        avail_fund = []
        dummy = []
        # for index in xrange(len(clients)):
        #     mafs = MAF.objects.filter(maf_client=clients[index]).last()
        #     if mafs is None or mafs == 0.00:
        #         pass
        #     else:
        #         avail_fund.append(mafs.maf_client)
        #         dummy.append(mafs.maf_total)
        choice = request.POST.get('dead')
        if choice == 'Client':
            # release curr_client MAF (all)
            client_acct = ReleaseMAFall(curr_client.cust_number)

            # declare Inactive
            curr_client.client_status = "Inactive"
            curr_client.save()
            # enable

            contrib_accts = ReleaseMAF_cl(curr_client)
            
            success = "All {}'s MAF has been successfully released.".format(curr_client)
            addl = ['Client account is now Inactive.', "All the client's accounts are now frozen.", "Client MAF: {}".format(client_acct), "Other members' contribution: {}.00".format(contrib_accts)]
            return render(request, 'success.html', {'success':success, 'list':addl})
        elif choice == 'Spouse':
            # subtract all clients except curr_client
            tots = ReleaseMAF_benef(curr_client, choice)

            success = "MAF has been successfully released for {}'s spouse.".format(curr_client)
            addl = ['All clients with MAF has been deducted Php 50.00', 'Total release: {}'.format(tots)]
            return render(request, 'success.html', {'success':success, 'list':addl})
        elif choice == 'Heirs':
            # subtract all clients except curr_client
            ReleaseMAF_benef(curr_client, choice)

            success = "MAF has been successfully released for {}'s heir.".format(curr_client)
            addl = ['All clients with MAF has been deducted Php 25.00']
            return render(request, 'success.html', {'success':success, 'list':addl})


def ReleaseMAFall(arg):
    """Release all client MAF. Accesses only the deceased client's MAF records"""
    client = Client.objects.get(cust_number=arg)
    fund = MAF.objects.filter(maf_client=client).last()
    if fund is None:
        print "no MAF"
    elif fund.maf_total == 0.00:
        data = {
            'maf_client':client,
            'maf_contrib_date':datetime.datetime.today().date(),
            'maf_ref': 'MAF account closed; client deceased.',
            'maf_debit': 0.00,
            'maf_credit': '',
            'maf_total': 0.00
        }
        forms = MAFform(data)
        if forms.is_valid():
            forms.save()
            # enable
        else:
            print forms.errors
    else:
        temp = fund.maf_total
        data = {
            'maf_client':fund.maf_client.cust_number,
            'maf_contrib_date':datetime.datetime.today().date(),
            'maf_ref': 'MAF account closed; client deceased.',
            'maf_debit': fund.maf_total,
            'maf_credit': '',
            'maf_total': (float(fund.maf_total)-float(fund.maf_total))
        }
        forms = MAFform(data)
        if forms.is_valid():
            forms.save()
            # enable
        else:
            print forms.errors
    return temp


def ReleaseMAF_cl(arg):
    """Subtracts Php100.00 from all members with MAF contribution,
    if 0.00 or MAF DoesNotExist: pass"""
    clients = Client.objects.filter(client_status="Active")

    total_release = []
    
    for index in xrange(len(clients)):
        mafs = MAF.objects.filter(maf_client=clients[index]).last()
        if mafs is None or mafs.maf_total == 0.00 or mafs.maf_total < 100.00:
            continue
        else:
            data = {
                'maf_client':mafs.maf_client.cust_number,
                'maf_contrib_date':datetime.datetime.today().date(),
                'maf_ref': 'MAF release for {} (deceased)'.format(arg),
                'maf_debit': 100.00,
                'maf_credit': '',
                'maf_total': (float(mafs.maf_total)-float(100.00))
            }
            forms = MAFform(data)

        if forms.is_valid():
            forms.save()
            # enable
            total_release.append(100)
            print "success"
        else:
            print "error"
            print forms.errors
    return sum(total_release)

def ReleaseMAF_benef(*args):
    """Subtracts Php50.00 from all members with MAF contribution,
    if 0.00 or MAF DoesNotExist: pass"""
    clients = Client.objects.filter(client_status="Active")

    total_release = []

    if args[1] == 'Spouse':
        for index in xrange(len(clients)):
            mafs = MAF.objects.filter(maf_client=clients[index]).last()
            if mafs is None or mafs.maf_total == 0.00 or mafs.maf_total < 50.00:
                continue
            elif args[0].cust_number == mafs.maf_client.cust_number:
                # print 'curr_client: {}'.format(arg)
                continue
            else:
                # print 'client: {} - {}'.format(clients[index], mafs.maf_client)
                # print 'index: {}'.format(index)
                data = {
                    'maf_client':mafs.maf_client.cust_number,
                    'maf_contrib_date':datetime.datetime.today().date(),
                    'maf_ref': 'MAF release for {}\'s spouse (deceased)'.format(args[0]),
                    'maf_debit': 50.00,
                    'maf_credit': '',
                    'maf_total': (float(mafs.maf_total)-float(50.00))
                }
                forms = MAFform(data)

            if forms.is_valid():
                forms.save()
                # enable
                total_release.append(50)
                print "success"
            else:
                print "error"
                print forms.errors
        print total_release
        return sum(total_release)
    else:
        for index in xrange(len(clients)):
            mafs = MAF.objects.filter(maf_client=clients[index]).last()
            if mafs is None or mafs.maf_total == 0.00 or mafs.maf_total < 25.00:
                continue
            elif args[0].cust_number == mafs.maf_client.cust_number:
                # print 'curr_client: {}'.format(arg)
                continue
            else:
                data = {
                    'maf_client':mafs.maf_client.cust_number,
                    'maf_contrib_date':datetime.datetime.today().date(),
                    'maf_ref': 'MAF release for {}\'s heir (deceased)'.format(args[0]),
                    'maf_debit': 25.00,
                    'maf_credit': '',
                    'maf_total': (float(mafs.maf_total)-float(25.00))
                }
                forms = MAFform(data)

            if forms.is_valid():
                forms.save()
                # enable
                total_release.append(25)
                print "success"
            else:
                print "error"
                print forms.errors
        print total_release
        return sum(total_release)
    


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
        client_id = int(self.kwargs.get('id'))
        user_input = request.POST['odf_credit']
        print self.kwargs.get('id')
        # forms = ODFform(request.POST) #get form data

        try:   #go here if model already has data
            #fetch last data from total field
            ref = ODF.objects.filter(odf_client=client_id).last()   #returns last odf_total
            if user_input:
                cred = float(request.POST.get('odf_credit'))   #convert user input(unicode) to float
                ref = float(ref.odf_total)   #convert queryset item to float
                tot = ref + cred   #we use float to accomodate centavos
                print 'tot: {}'.format(tot)
                data = {
                    'odf_client': request.POST.get('odf_client'),
                    'odf_contrib_date':request.POST.get('odf_contrib_date'),
                    'odf_ref':'deposit',
                    'odf_debit':'',
                    'odf_credit':cred,
                    'odf_total': tot
                    }
                forms = ODFform(data)
            else:
                error = 'Please fill the form properly'
                list2 = ['no input value at Credit']
                return render(request, 'success.html', {'error':error, 'list':list2})
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
        print 'ref: {}'.format(ref)
        if forms.is_valid():
            forms.save()
            success = 'ODF contribution recorded'
            return render(request, 'success.html', {'success':success})
        else:
            error = 'Please fill the form properly'
            return render(request, 'success.html', {'error':error, 'list':forms.errors})

    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id, client_status="Active")
        form = ODFform(initial={'odf_client': client})
        form.fields['odf_client'].widget.attrs['readonly'] = True
        form.fields['odf_contrib_date'].widget.attrs['readonly'] = True
        return render(request, 'cashier_odfpay.html', {'form':form, 'Client':client})


class ReleaseODFSearch(TemplateView):
    """Searches only clients with ODF != 0.00"""
    # template_name = 'cashier_odf_release.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'cashier_odfrelease_search.html')

    def post(self, request, *args, **kwargs):
        client = Client.objects.filter(
            lastname__contains=request.POST['search'],
            client_status="Active"
            )
        # products = ODF.objects.filter(odf_client=client).last()
        products = []
        if client:
            for index in xrange(len(client)):
                odfs = ODF.objects.filter(odf_client=client[index]).last()
                print odfs
                if odfs != None:
                    products.append(odfs)
                else:
                    pass
            return render(request, 'cashier_odfrelease_search.html', {'object_list':products})
        else:
            messages.error(request, 'Search returned nothing. Client does not exist or ODF contributions does not exist')
            return render(request, 'cashier_odfrelease_search.html')


class ReleaseODFView(View):


    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id, client_status="Active")
        fund = ODF.objects.filter(odf_client__cust_number=client_id)
        return render(request, 'cashier_odfrelease_view.html', {'object_list':fund, 'client':client})


class ReleaseODFForm(View):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id, client_status='Active')
        form = ODFform(initial={'odf_client':client, 'odf_ref':'Withdrawal'})
        form.fields['odf_client'].widget.attrs['readonly'] = True
        form.fields['odf_contrib_date'].widget.attrs['readonly'] = True
        return render(request, 'cashier_odfrelease_form.html', {'form':form})

    def post(self, request, *args, **kwargs):
        client_id = int(self.kwargs.get('id'))
        client = Client.objects.get(cust_number=client_id, client_status='Active')
        # form = ODFform(initial={'odf_client':client})
        forms = ODFform(request.POST)

        try:
            ref = ODF.objects.filter(odf_client=client).last()   #returns last odf_total
            if float(request.POST.get('odf_debit')) > float(ref.odf_total):
                error = "Withdrawal amount is greater than remaining ODF balance"
                list2 = ['ODF balance: {}'.format(ref.odf_total)]
                return render(request, 'success.html', {'error':error, 'list':list2})
            else:
                deb = float(request.POST['odf_debit'])   #convert user input(unicode) to float
                ref = float(ref.odf_total)   #convert queryset item to float
                tot = ref - deb   #we use float to accomodate centavos
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
            error = 'Please fill the form properly'
            list2 = ['Debit field empty']
            return render(request, 'success.html', {'error':error, 'list':list2})

        if forms.is_valid():
            forms.save()
            success = 'ODF release recorded'
            return render(request, 'success.html', {'success':success})
        else:
            error = 'Please fill the form properly'
            list2 = ['Debit field empty']
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
        user_input = request.POST['savings_credit']

        try:
            ref = Savings.objects.filter(savings_client__cust_number=client_id).last()
            if user_input:
                cred = float(user_input)
                print cred
                ref = float(ref.savings_total)
                tot = ref + cred

                data = {
                    'savings_client': request.POST.get('savings_client'),
                    'savings_contrib_date': request.POST.get('savings_contrib_date'),
                    'savings_ref': 'deposit',
                    'savings_debit': '',
                    'savings_credit': cred,
                    'savings_total': tot
                }
                forms = SavingsForm(data)
            else:
                error = 'Please fill form properly'
                list2 = ['no input amount at Credit']
                return render(request, 'success.html', {'error':error, 'list':list2})

        except:
            data = {
                'savings_client': request.POST.get('savings_client'),
                'savings_contrib_date': request.POST.get('savings_contrib_date'),
                'savings_ref': 'forwarded balance',
                'savings_debit': '',
                'savings_credit': request.POST.get('savings_credit'),
                'savings_total': request.POST.get('savings_credit')
            }
            forms = SavingsForm(data)

        if forms.is_valid():
            forms.save()
            success = 'Savings contribution saved'
            return render(request, 'success.html', {'success':success})
        else:
            error = 'Please fill form properly'
            list2 = ['no input amount at Credit']
            return render(request, 'success.html', {'error':error, 'list':list2})


    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id)
        form = SavingsForm(initial={'savings_client': client})
        form.fields['savings_client'].widget.attrs['readonly'] = True
        form.fields['savings_contrib_date'].widget.attrs['readonly'] = True
        return render(request, 'cashier_savingsAdd.html', {'form':form})


class SavingsReleaseSearch(TemplateView):
    """Cashier/Admin access only. Returns client accts with savings only"""

    def get(self, request, *args, **kwars):
        return render(request, 'cashier_savingsReleaseSearch.html')


    def post(self, request, *args, **kwargs):
        client = Client.objects.filter(
            lastname__contains=request.POST['search'],
            client_status="Active"
        )
        products = []
        if client:
            for index in xrange(len(client)):
                sav = Savings.objects.filter(savings_client=client[index]).last()
                if sav != None:
                    products.append(sav)
                else:
                    pass
            return render(request, 'cashier_savingsReleaseSearch.html', {'object_list':products})
        else:
            messages.error(request, 'Search returned nothing. Client or Savings does not exist.')
            return render(request, 'cashier_savingsReleaseSearch.html')



class SavingsRelease(View):


    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id, client_status="Active")
        fund = Savings.objects.filter(savings_client__cust_number=client_id)
        return render(request, 'cashier_savings_release.html', {'object_list':fund, 'client':client})



class SavingsReleaseForm(View):

    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client = Client.objects.get(cust_number=client_id)
        fund = Savings.objects.filter(savings_client__cust_number=client_id).last()
        form = SavingsForm(initial={'savings_client': client, 'savings_ref':'Withdrawal'})
        form.fields['savings_client'].widget.attrs['readonly'] = True
        form.fields['savings_contrib_date'].widget.attrs['readonly'] = True
        return render(request, 'cashier_savings_release_form.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = SavingsForm()
        client_id = int(kwargs.get('id'))
        client = Client.objects.get(cust_number=client_id)
        fund = Savings.objects.filter(savings_client=client_id, savings_client__client_status="Active").last()
        user_input = request.POST.get('savings_debit')
        print fund.savings_total
        if user_input:
            if float(user_input) > float(fund.savings_total):
                error = "Withdrawal amount is greater than remaining Savings balance"
                list2 = ['Savings balance: {}'.format(fund.savings_total)]
                return render(request, 'success.html', {'error':error, 'list':list2})
            elif float(request.POST.get('savings_debit') < 0.00):
                error = "Does not allow Withdrawal of negative values"
                return render(request, 'success.html', {'error':error})
            elif float(request.POST['savings_debit']) <= float(fund.savings_total):
                deb = float(request.POST['savings_debit'])
                ref = float(fund.savings_total)
                tot = ref - deb

                data = {
                    'savings_client': client_id,
                    'savings_contrib_date': datetime.datetime.today().date(),
                    'savings_ref': 'Savings Withdrawal',
                    'savings_debit': request.POST['savings_debit'],
                    'savings_credit': '',
                    'savings_total': tot
                }

                form = SavingsForm(data)
        else:
            error = "No amount at debit field."
            return render(request, 'success.html', {'error':error})

        if form.is_valid():
            form.save()
            success = 'Savings release recorded'
            return render(request, 'success.html', {'success':success})
        else:
            print 'invalid form'
            error = 'Please fill the form properly'
            return render(request, 'success.html', {'error':error, 'list':form.errors})


class PayStructFeeSearch(TemplateView):
    """Cashier/Admin access only. Returns loan_apps and restructs that are pending"""

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'cashier_paystructfee_search.html')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        products = Restruct.objects.filter(loan_root__client__lastname__contains=request.POST['search'], approval_status=True)
        if products:
            return render(request, 'cashier_paystructfee_search.html', {'object_list':products})
        else:
            messages.error(request, 'Search returned nothing. Client does not exist or Restructure object does not exist')
            return render(request, 'cashier_paystructfee_search.html')



class PayStructFee(View):
    """Cashier/Admin access only. Returns restruct_id"""

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        struct = Restruct.objects.get(loan_root__client__cust_number=client_id, approval_status=True, restruct_status='Pending')
        print "struct_id: {}".format(struct.id)
        print "loan_app_id from struct: {}".format(struct.loan_root.app_id)
        print "cust_number from struct: {}".format(struct.loan_root.client.cust_number)
        # we get only one because User already selected from the search menu
        return render(request, "cashier_paystructfee.html", {'objects':struct})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        struct = Restruct.objects.get(loan_root__client__cust_number=client_id, approval_status=True, restruct_status='Pending')
        loan_app = loanApplication.objects.get(app_id=struct.loan_root.app_id)
        print "struct_id: {}".format(struct.id)
        print "loan_app_id: {}".format(loan_app.app_id)

        if request.POST.get('submit') == 'pay':
            print "if"
            struct.restruct_fee = request.POST['fee']
            struct.restruct_status = 'Outstanding'
            struct.save()
            success = "Payment Successful"
            return render(request, 'success.html', {'success':success})
        elif request.POST.get('submit') == 'reject':
            print "elif"
            struct.approval_status = False
            print struct.loan_root.app_id
            # loan_app = loanApplication.objects.get(app_id=struct.loan_root.app_id)
            # struct2 = Restruct.entry_set
            print loan_app.app_id
            
            loan_app.app_status = 'Denied'
            struct.save()
            loan_app.save()
            success = "Restructure was rejected"
            return render(request, 'success.html', {'success':success})
        else:
            return HttpResponse(request.POST)



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
                # create loan application
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
                else:
                    pass
                
                # create restruct
                struct_fee = (tot * 0.015) + 50.00
                new_loan_app = loanApplication.objects.get(restruct=True, client=loan_id.client.cust_number, app_date=datetime.datetime.today().date())
                info1 = {
                    'loan_root': new_loan_app.app_id,
                    'loan_in_interest': loan_in,
                    'loan_in_amount': loan_ledger_in.total_loan_recievable,
                    'loan_over_interest': loan_over,
                    'loan_over_amount': loan_ledger_out.total_loan_recievable,
                    'restruct_fee': struct_fee
                }
                struct1 = RestructForm(info1)
                if struct1.is_valid():
                    struct1.save()
                    loan_id.overdue = False
                    loan_id.loan_status = 'Restructured'
                    loan_id.save()
                else:
                    pass

            elif loan_over == 0.0:
                # 1.5 x 0.0
                # existing loan is within CBU at the time of application/approval
                loan_ledger_in = payLoanLedger_in.objects.filter(client=loan_id).last()
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
                else:
                    pass
                
                struct_fee = (tot * 0.015) + 50.00
                new_loan_app = loanApplication.objects.get(restruct=True, client=loan_id.client.cust_number, app_date=datetime.datetime.today().date())
                info1 = {
                    'loan_root': new_loan_app.app_id,
                    'loan_in_interest': loan_in,
                    'loan_in_amount': loan_ledger_in.total_loan_recievable,
                    'loan_over_interest': 0,
                    'loan_over_amount': 0,
                    'restruct_fee': struct_fee
                }
                struct1 = RestructForm(info1)
                if struct1.is_valid():
                    struct1.save()
                    loan_id.overdue = False
                    loan_id.loan_status = 'Restructured'
                    loan_id.save()
                else:
                    pass

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
                else:
                    pass

                struct_fee = (tot * 0.015) + 50.00
                new_loan_app = loanApplication.objects.get(restruct=True, client=loan_id.client.cust_number, app_date=datetime.datetime.today().date())
                info2 = {
                    'loan_root': new_loan_app.app_id,
                    'loan_in_interest': loan_in,
                    'loan_in_amount': loan_ledger_in.total_loan_recievable,
                    'loan_over_interest': loan_over,
                    'loan_over_amount': loan_ledger_out.total_loan_recievable,
                    'restruct_fee': struct_fee
                }
                struct2 = RestructForm(info2)
                if struct2.is_valid():
                    struct2.save()
                    loan_id.overdue = False
                    loan_id.loan_status = 'Restructured'
                    loan_id.save()
                else:
                    pass

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
                else:
                    pass

                struct_fee = (tot * 0.015) + 50.00
                new_loan_app = loanApplication.objects.get(restruct=True, client=loan_id.client.cust_number, app_date=datetime.datetime.today().date())
                info2 = {
                    'loan_root': new_loan_app.app_id,
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
                    pass
            else:
                # does not exist
                print 'no update'
                pass

    except:
        error = 'Fatal Error. Loan could not be restructured.'
        return render(request, 'success.html', {'error': error})

    return HttpResponseRedirect(reverse('profile', kwargs={'id':loan_id.client.cust_number}))