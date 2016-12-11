from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator

optional = {
    'null': True,
    'blank': True
}

#NO CUSTOMER PHONE NUMBER, CAPITAL, ODF, MAF
# Create your models here.
class Client(models.Model):

    SINGLE='Single'
    MARRIED='Married'
    WIDOWED='Widowed'
    SEPARATED='Separated'
    WIFE='Wife'
    PARENTS='Parents'
    GRADESCHOOL='Grade School'
    HIGHSCHOOL='High School'
    COLLEGEGRADUATE='College Graduate'
    COLLEGEUNDERGRADUATE='College Undergraduate'
    DRIVER='Driver'
    OPERATOR='Operator'
    ALLIEDWORKER='Allied Worker'
    ACTIVE='Active'
    INACTIVE='Inactive'
    SSS='SSS'
    TIN='TIN'
    OTHERS='Others'
    WAITING='Waiting'
    DENIED='Denied'
    APPROVED='Approved'


    APP_STATUS = (
        (WAITING, 'Waiting'),
        (DENIED, 'Denied'),
        (APPROVED, 'Approved'),

        )


    CS = (
        (SINGLE, 'Single'),
        (MARRIED, 'Married'),
        (WIDOWED, 'Widowed'),
        (SEPARATED, 'Separated'),
    )


    EA = (
        (GRADESCHOOL, 'Grade School'),
        (HIGHSCHOOL, 'High School'),
        (COLLEGEGRADUATE, 'College Graduate'),
        (COLLEGEUNDERGRADUATE, 'College Undergraduate'),
    )


    MT = (
        (DRIVER, 'Driver'),
        (OPERATOR, 'Operator'),
        (ALLIEDWORKER, 'Allied Worker'),
    )


    CUST_STATUS = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )



    ID_TYPE = (
        (SSS, 'SSS'),
        (TIN, 'TIN'),
        (OTHERS, 'Others'),
    )



    BENFICIARY = (
        (SINGLE, 'Single'),
        (WIFE, 'Wife'),
        (PARENTS, 'Parents'),
    )


    cust_number = models.AutoField(primary_key=True)
    join_date = models.DateField('Joined Date: ', default=datetime.now, blank=True)
    firstname = models.CharField(max_length=99, null=False, default="")
    middlename = models.CharField(max_length=99, null=False, default="")
    lastname = models.CharField(max_length=99, null=False, default="")
    age = models.PositiveIntegerField(default=18, null=False, validators=[MinValueValidator(18)])
    civil_status = models.CharField(
        choices=CS,
        default=SINGLE,
        max_length=10,
        )
    phone_number = models.CharField(max_length=11, blank=True)
    address = models.CharField(max_length=99, null=False, default="Davao City")
    birthdate = models.DateField(blank=True, null=False, default=datetime.now)
    educ_attain = models.CharField(
        choices=EA,
        default=COLLEGEGRADUATE,
        max_length=22,
        )
    occupation = models.CharField(max_length=99, default="")
    membership_type = models.CharField(
        choices=MT,
        default=ALLIEDWORKER,
        null=False,
        max_length=13,
        )
    client_status = models.CharField(
        choices=CUST_STATUS,
        default=ACTIVE,
        null=False,
        max_length=9,
        )
    capital = models.DecimalField(max_digits=8, decimal_places=2, blank=True, validators=[MinValueValidator(0.01)])
    client_id_type = models.CharField(
        choices=ID_TYPE,
        default=SSS,
        null=False,
        max_length=7,
        )
    client_id_number = models.CharField(max_length=20, default="")
    client_odf = models.DecimalField(max_digits=8, decimal_places=2, blank=True, validators=[MinValueValidator(0.01)])
    client_maf = models.DecimalField(max_digits=8, decimal_places=2, blank=True, validators=[MinValueValidator(0.01)])
    beneficiary = models.CharField(
        choices=BENFICIARY,
        default=SINGLE,
        null=False,
        max_length=8,
        )

    def __unicode__(self):
        return u'%s, %s' % (self.lastname, self.firstname)


class loanApplication(models.Model):
    providentialLoan='Providential Loan'
    emergencyLoan='Emergency Loan'
    pending='Pending'
    denied='Denied'
    approved='Approved'
    Status = (
        (pending, 'Pending'),
        (denied, 'Denied'),
        (approved, 'Approved'),
    )
    kind = (
    (providentialLoan,'Providential Loan'),
    (emergencyLoan,'Emergency Loan'),
    )
    client=models.ForeignKey(Client)
    app_id=models.AutoField(primary_key=True)
    app_date=models.DateField('Date of application: ', default=datetime.now)
    app_status=models.CharField(
        choices=Status,
        default=pending,
        max_length=15,
        )
    app_kind=models.CharField(
        choices = kind,
        default = providentialLoan,
        max_length=20,
        )
    app_amount=models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    app_comaker=models.ForeignKey(Client, related_name='Comaker', blank=True, null=True)
    approval_date = models.DateField(**optional)

    def __unicode__(self):
        return '%s' % (self.client)


class LoanInformation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(**optional)

    def __unicode__(self):
        return self.name


class Collateral(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(**optional)
    value = models.DecimalField(max_digits=8, decimal_places=1, blank=True, validators=[MinValueValidator(0.1)])



class Loan(models.Model):
    type_of_loan = models.CharField(max_length=12, choices=(
        ('Providential', "Providential"),
        ('Emergency', "Emergency")
        ))
    client = models.ForeignKey('Client')
    loan_application = models.OneToOneField('loanApplication')
    loan_information = models.ManyToManyField('LoanInformation')
    loan_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, validators=[MinValueValidator(0.01)])
    interest_rate = models.DecimalField(max_digits=8, decimal_places=1, blank=True, validators=[MinValueValidator(0.1)])
    loan_duration = models.PositiveIntegerField()
    loan_status = models.CharField(max_length=11, choices=(
        ('Outstanding', "Outstanding"),
        ('Paid', "Paid")
        ), default="Outstanding")
    check_number = models.CharField(max_length=50, **optional)
    collateral = models.ForeignKey('Collateral', **optional)

    def __unicode__(self):
        return "{} - {}".format(self.client, self.loan_application.approval_date)

class payLoan(models.Model):
    maf='MAF'
    odf='ODF'
    loan='Loan'
    cash='Cash'
    cheque='Cheque'

    ptype=(
        (cash, 'Cash'),
        (cheque, 'Cheque'),
        )

    pfor=(
        (loan, 'Loan'),
        (maf, 'MAF'),
        (odf, 'ODF'),
        )

    client=models.ForeignKey(Client)
    pay_id=models.AutoField(primary_key=True)
    pay_amount=models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    pay_trans_date=models.DateField(default=datetime.now)
    pay_type=models.CharField(
        choices=ptype,
        default=cash,
        max_length=7,
        )
    pay_for=models.CharField(
        choices=pfor,
        default=loan,
        max_length=5,
        )


    def __unicode__(self):
        return "%s" (self.client)