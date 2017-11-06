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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from clients.forms import ClientForm
from vamps import views, tasks

admin.autodiscover()

urlpatterns = [
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
    url(r'^home/cashier/add-savings-search/$', views.SavingsAddSearch.as_view(), name="add_savings_search"),
    url(r'^home/cashier/add-savings-search/add-savings/(?P<id>\w+)', views.SavingsAdd.as_view(), name="add_savings"),
    url(r'^home/cashier/release-savings-search/$', views.SavingsReleaseSearch.as_view(), name="release_savings_search"),
    url(r'^home/cashier/release-savings-search/release-savings/(?P<id>\w+)', views.SavingsRelease.as_view(), name="release_savings"),
    url(r'^home/cashier/release-savings-search/release_savings/release-savings-form/(?P<id>\w+)', views.SavingsReleaseForm.as_view(), name="release_savings_form"),

    url(r'^home/bookkeeper/$', views.bookkeeper.as_view(), name="book_menu"),
    url(r'^home/bookkeeper/add-new-client/$', views.add_client.as_view(), name="add_new_client"),
    url(r'^home/bookkeeper/create-loan/(?P<id>\w+)', views.CreateLoan.as_view(), name="create_loan"),

    url(r'^home/web-admin/$', views.admin_page.as_view(), name="admin_page"),
    url(r'^home/web-admin/user-lists/$', views.UserViewFilter.as_view(), name='users'),
    url(r'^edit-profile/$', views.Modify.as_view(), name="edit_profile"),
    url(r'^restricted/$', views.restricted, name="restricted"),
    url(r'^profile-lists/$', views.ClientViewFilter.as_view(), name="profile_search"),
    url(r'^clients-list/$', views.ClientList.as_view(), name='clients_list'),
    url(r'^old-loan-search/$', views.ViewOldLoanSearch.as_view(), name="old_loan_search"),
    url(r'^view-old-loan/(?P<id>\w+)', views.ViewOldLoan.as_view()),
    url(r'^add-new-loan-application/(?P<id>\w+)', views.loan_application.as_view(), name="new_loan"),
    url(r'^approve-loan-application/approve/(?P<id>\w+)', views.approve_loan_application),
    url(r'^approve-loan-application/reject/(?P<id>\w+)', views.reject_loan_application),
    url(r'^update/(?P<id>\w+)', views.update),
    url(r'^restructure/(?P<id>\w+)', views.restruct),
    url(r'^home/cashier/pay-structfee-search/$', views.PayStructFeeSearch.as_view(), name="pay_structfee_search"),
    url(r'^home/cashier/pay-structfee-search/pay-structfee/(?P<id>\w+)', views.PayStructFee.as_view()),
]
