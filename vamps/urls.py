"""vamps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
<<<<<<< HEAD
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from clients.forms import ClientForm
from vamps import views, tasks
=======
# from django.conf import settings
# from django.conf.urls import (include, patterns, url)
# from django.conf.urls.static import static
# from django.contrib import admin
# from django.views.generic import TemplateView
from django.conf.urls import url, include
from django.contrib import admin

from django.views.generic import TemplateView

from vamps import views
from .views import(
    UsersView,
    login_user,
    cashier,
    bookkeeper,
    add_new_client,
    admin_page,
    home,
    register,
    register_success,
    logout_page,
    add_new_client,
    add_client,
    restricted,
    ClientView,
    #search,
    ClientViewFilter,
    ClientViewFilterOne,
    # SearchClient,
    loan_application,
    pay_loan,
    write_receipt,
    )

>>>>>>> 549418614833c8e5b4d8caf88e6746fdc1fb1760

admin.autodiscover()

urlpatterns = [
<<<<<<< HEAD
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login_user, name="home"), # used at base
    # url(r'^home/$', views.home, name="homepage"), # not used
    url(r'^$', views.login_user), # alternate for home
    url(r'^home/web-admin/register/$', views.register),
    # url(r'^home/web-admin/register/success/$', views.register_success),
    url(r'^logout/$', views.logout_page, name="logout"),
    url(r'^client-profile/(?P<id>\w+)', views.ClientProfile.as_view(), name="profile"),
    url(r'^home/cashier/$', views.cashier.as_view(), name="cashier_menu"),
    url(r'^home/cashier/pay-loan-search/$', views.PayLoanSearch.as_view(), name="loan_invoice"),
    url(r'^home/cashier/pay-loan-search/pay-loan-form/(?P<id>\w+)', views.PayLoan.as_view(), name="payloan"),
    url(r'^home/cashier/pay-maf-search/$', views.PayMAF.as_view(), name="pay_maf_search"),
    url(r'^home/cashier/pay-maf-search/pay-maf-form/(?P<id>\w+)', views.PayMAFform.as_view()),
    url(r'^home/cashier/maf-release-search/$', views.ReleaseMAFsearch.as_view(), name="release_maf_search"),
    url(r'^home/cashier/maf-release-search/maf-release/(?P<id>\w+)', views.ReleaseMAFform.as_view(), name="release_maf"),
    url(r'^home/cashier/pay-odf-search/$', views.PayODFsearch.as_view(), name="pay_odf_search"),
    url(r'^home/cashier/pay-odf-search/pay-odf-form/(?P<id>\w+)', views.PayODFform.as_view()),
    url(r'^home/cashier/release-odf-search/$', views.ReleaseODFSearch.as_view(), name="release_odf_search"),
    url(r'^home/cashier/release-odf-search/release-odf/(?P<id>\w+)', views.ReleaseODFForm.as_view()),
    url(r'^home/cashier/pay-cbu/$', views.PayCBU.as_view(), name="pay_cbu_search"),
    url(r'^home/cashier/pay-cbu/pay-cbu-form/(?P<id>\w+)', views.PayCBUform.as_view()),

    url(r'^home/bookkeeper/$', views.bookkeeper.as_view(), name="book_menu"),
    url(r'^home/bookkeeper/add-new-client/$', views.add_client.as_view(), name="add_new_client"),
    url(r'^home/bookkeeper/create-loan/(?P<id>\w+)', views.CreateLoan.as_view(), name="create_loan"),

    url(r'^home/web-admin/$', views.admin_page.as_view(), name="admin_page"),
    url(r'^home/web-admin/user-lists/$', views.UserViewFilter.as_view(), name='users'),
    url(r'^edit-profile/$', views.Modify.as_view(), name="edit_profile"),
    url(r'^restricted/$', views.restricted, name="restricted"),
    url(r'^client-lists/$', views.ClientViewFilter.as_view(), name="profile_search"),
    url(r'^old-loan-search/$', views.ViewOldLoanSearch.as_view(), name="old_loan_search"),
    url(r'^view-old-loan/(?P<id>\w+)', views.ViewOldLoan.as_view()),
    url(r'^add-new-loan-application/(?P<id>\w+)', views.loan_application.as_view(), name="new_loan"),
    url(r'^approve-loan-application/approve/(?P<id>\w+)', views.approve_loan_application),
    url(r'^approve-loan-application/reject/(?P<id>\w+)', views.reject_loan_application),
    url(r'^update/(?P<id>\w+)', views.update),
    url(r'^restructure/(?P<id>\w+)', views.restruct),
    url(r'^home/cashier/pay-structfee-search/$', views.PayStructFeeSearch.as_view(), name="pay_structfee_search"),
    url(r'^home/cashier/pay-structfee-search/pay-structfee/(?P<id>\w+)', views.PayStructFee.as_view()),
=======
    # url(r'^$', login.as_view(), name="register"),
    # url(r'^admin/', admin.site.urls),
    # url(r'^cashier/$', cashier.as_view(), name="cashier_menu"),
    # url(r'^bookkeeper/$', bookkeeper.as_view(), name="book_menu"),
    # url(r'^add_new/$', add_new_client.as_view(), name="new_client"),
    # url(r'^success/$', success.as_view(), name="success"),
    url(r'^admin/', admin.site.urls),
    url(r'^$', login_user, name="home"),
    url(r'^home/$', home),
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page, name="logout"),
    url(r'^cashier/$', cashier.as_view(), name="cashier_menu"),
    url(r'^bookkeeper/$', bookkeeper.as_view(), name="book_menu"),
    url(r'^web-admin/$', admin_page.as_view(), name="admin_page"),
    url(r'^user-lists/$', views.UsersView.as_view(), name='users'),
    url(r'^edit_profile/$', views.Modify.as_view()),
    url(r'^add-new-client/$', views.add_client.as_view()),
    url(r'^logout/$', restricted),
    url(r'^client-lists/$', views.ClientViewFilter.as_view()),
   # url(r'^results/$', search),
    url(r'^results/$', ClientViewFilter.as_view()),
    # url(r'^search-client/$', SearchClient.as_view()),
    url(r'^create-loan/(?P<id>\w+)', views.CreateLoan.as_view(), name="create_loan"),
    url(r'^view-loan/(?P<id>\w+)', views.ViewLoanInformation.as_view(), name="view_loan"),
    url(r'^add-new-loan-application/$', views.loan_application.as_view()),
    url(r'^approve-loan-application/$', views.LoanApproval.as_view(), name="approve_loan_app"),
    url(r'^approve-loan-application/approve/(?P<id>\w+)', views.approve_loan_application),
    url(r'^approve-loan-application/reject/(?P<id>\w+)', views.reject_loan_application),
    url(r'^pay-loan/$', views.pay_loan.as_view(), name="invoice"),
    url(r'^print-receipt/$', views.render_receipt),
    url(r'^write-receipt/$', views.write_receipt.as_view()),

>>>>>>> 549418614833c8e5b4d8caf88e6746fdc1fb1760
]
