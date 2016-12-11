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


admin.autodiscover()

urlpatterns = [
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

]
