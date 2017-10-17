from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.core.validators import MinValueValidator

optional = {
    'null': True,
    'blank': True
}

class Client(models.Model):

    SINGLE='Single'
    MARRIED='Married'
    WIDOWED='Widowed'
    SEPARATED='Separated'
    SPOUSE='Spouse'
    PARENTS='Parents'
    HEIRS='Heirs'
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

    # unused
    WAITING='Waiting'
    DENIED='Denied'
    APPROVED='Approved'


    # unused
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
        (SPOUSE, 'Spouse'),
        (PARENTS, 'Parents'),
        (HEIRS, 'Heirs')
    )


    cust_number = models.AutoField(primary_key=True)
    join_date = models.DateField(
        'Joined Date: ',
        default=datetime.now,
        blank=True)
    firstname = models.CharField(
        max_length=99,
        null=False,
        default="")
    middlename = models.CharField(
        max_length=99,
        null=False,
        default="")
    lastname = models.CharField(
        max_length=99,
        null=False,
        default="")
    age = models.PositiveIntegerField(
        default=18,
        null=False,
        validators=[MinValueValidator(18)])
    civil_status = models.CharField(
        choices=CS,
        # default=SINGLE,
        max_length=10,
        )
    phone_number = models.CharField(
        max_length=11,
        blank=True)
    address = models.CharField(
        max_length=99,
        null=False,
        default="Davao City")
    birthdate = models.DateField(
        blank=True,
        null=False,
        # default=datetime.now
        )
    educ_attain = models.CharField(
        choices=EA,
        default=COLLEGEGRADUATE,
        max_length=22,
        )
    occupation = models.CharField(
        max_length=99,
        default="")
    membership_type = models.CharField(
        choices=MT,
        # default=ALLIEDWORKER,
        null=False,
        max_length=13,
        )
    client_status = models.CharField(
        choices=CUST_STATUS,
        default=ACTIVE,
        null=False,
        max_length=9,
        )
    client_id_type = models.CharField(
        choices=ID_TYPE,
        # default=SSS,
        null=False,
        max_length=7,
        )
    client_id_number = models.CharField(
        max_length=20,
        default="")
    beneficiary = models.CharField(
        choices=BENFICIARY,
        # default=SINGLE,
        null=False,
        max_length=8,
        )

    def __unicode__(self):
        return u'%s, %s' % (self.lastname, self.firstname)



class client_capital(models.Model):
    cap_client=models.ForeignKey(Client)
    cap_id=models.AutoField(primary_key=True)
    cap_contrib_date=models.DateField(
        'Date of Contribution: ',
        default=datetime.now
        )
    cap_contrib=models.DecimalField(    # added to capital
        max_digits=8,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0.01)]
        )
    capital=models.DecimalField(    # total capital
        max_digits=8,
        decimal_places=2,
        blank=True,
        default=0,
        validators=[MinValueValidator(0.01)]
        )

    def __unicode__(self):
        return u'%s' % (self.capital)



class loanApplication(models.Model):
    providentialLoan='Providential Loan'
    emergencyLoan='Emergency Loan'
    pending='Pending'
    denied='Denied'
    approved='Approved'
    done='Paid'
    Status = (
        (pending, 'Pending'),
        (denied, 'Denied'),
        (approved, 'Approved'),
        (done, 'Paid')
    )
    kind = (
    (providentialLoan,'Providential Loan'),
    (emergencyLoan,'Emergency Loan'),
    )
    client=models.ForeignKey(Client)
    app_id=models.AutoField(primary_key=True)
    app_date=models.DateField(
        'Date of application', 
        default=datetime.now)
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
    app_amount=models.DecimalField(
        max_digits=8,
        decimal_places=2, 
        validators=[MinValueValidator(0.01)]
        )
    app_comaker=models.ForeignKey(
        Client, 
        related_name='Comaker', 
        **optional
        )
    approval_date = models.DateField(**optional)
    restruct = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.client)



class Restruct(models.Model):
    loan_root = models.ForeignKey(loanApplication, related_name='app_root')
    loan_in_interest = models.DecimalField(
        max_digits=8, 
        decimal_places=1, 
        blank=True, 
        validators=[MinValueValidator(0.1)]
    )
    loan_in_amount = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True,
        validators=[MinValueValidator(0.01)]
    )
    loan_over_interest = models.DecimalField(
        max_digits=8, 
        decimal_places=1, 
        blank=True, 
        validators=[MinValueValidator(0.1)]
    )
    loan_over_amount = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True,
        validators=[MinValueValidator(0.01)]
    )
    restruct_fee = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True,
        default=50.00,
        validators=[MinValueValidator(0.01)]
    )
    approval_status = models.BooleanField(default=False)
    restruct_status = models.CharField(
        max_length=11, 
        choices=(
            ('Outstanding', "Outstanding"),
            ('Paid', "Paid"),
        ), 
        default="Outstanding")



class Collateral(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Client, **optional)
    description = models.TextField(**optional)
    val = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True, 
        validators=[MinValueValidator(0.01)]
    )



class Loan(models.Model):
    type_of_loan = models.CharField(max_length=12, choices=(
        ('Providential', "Providential"),
        ('Emergency', "Emergency")
        ))
    client = models.ForeignKey('Client')
    loan_application = models.OneToOneField('loanApplication')
    # loan_information = models.ManyToManyField('LoanInformation')
    loan_amount = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True,
        validators=[MinValueValidator(0.01)]
    )
    loan_overflow = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True, 
        # validators=[MinValueValidator(0.01)], 
        default=0
    )
    interest_rate = models.DecimalField(
        max_digits=8, 
        decimal_places=1, 
        blank=True, 
        validators=[MinValueValidator(0.1)]
    )
    interest_rate_over = models.DecimalField(
        max_digits=8, 
        decimal_places=1, 
        blank=True, 
        validators=[MinValueValidator(0.1)]
    )
    loan_duration = models.PositiveIntegerField()
    loan_status = models.CharField(
        max_length=11, 
        choices=(
            ('Outstanding', "Outstanding"),
            ('Paid', "Paid"),
            ('Restructured', "Restructured")
        ), 
        default="Outstanding")
    update = models.BooleanField(default=False)
    overdue = models.BooleanField(default=False)
    check_number = models.CharField(
        max_length=50,
         **optional)
    collateral = models.ForeignKey('Collateral', **optional)
    
    def __unicode__(self):
        return u'%s, %s' % (self.client, self.loan_amount + self.loan_overflow)

class payLoanLedger_in(models.Model):
    cash='Cash'
    cheque='Cheque'

    ptype=(
        (cash, 'Cash'),
        (cheque, 'Check'),
        )

    #ledger fields (may contain fields also associated with the receipt)
    client=models.ForeignKey(Loan)
    trans_date=models.DateField(
        default=datetime.now)
    reference=models.CharField(
        max_length=20,
        null=True,
        default="-")
    debit_loanGranted=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])
    credit_payment=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])
    int_per_month=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])
    total_loan_recievable=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=10,
        decimal_places=2,
        # validators=[MinValueValidator(0.01)]
    )
    #official receipt fields
    loan_pay_id=models.AutoField(primary_key=True)
    loan_pay_type=models.CharField(
        choices=ptype,
        default=cash,
        max_length=7,
        )
    loan_pay_received_by=models.CharField(
        max_length=15,
        default="Cashier",
        null=False)

    # def __unicode__(self):
    #     return u"%s, %s" %(self.client, self.pay_amount)
    #     return unicode(self.client, self.pay_amount)


class payLoanLedger_over(models.Model):
    cash='Cash'
    cheque='Cheque'

    ptype=(
        (cash, 'Cash'),
        (cheque, 'Check'),
        )

    #ledger fields (may contain fields also associated with the receipt)
    client=models.ForeignKey(Loan)
    trans_date=models.DateField(
        default=datetime.now)
    reference=models.CharField(
        max_length=20,
        null=True,
        default="-")
    debit_loanGranted=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])
    credit_payment=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])
    int_per_month=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])
    total_loan_recievable=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=10,
        decimal_places=2,
        # validators=[MinValueValidator(0.01)]
    )
    #official receipt fields
    loan_pay_id=models.AutoField(primary_key=True)
    loan_pay_type=models.CharField(
        choices=ptype,
        default=cash,
        max_length=7,
        )
    loan_pay_received_by=models.CharField(
        max_length=15,
        default="Cashier",
        null=False)

class MAF(models.Model):
    maf_client=models.ForeignKey(Client)
    maf_id=models.AutoField(primary_key=True)
    # maf_beneficiary=models.ForeignKey(Client.beneficiary)
    maf_contrib_date=models.DateField(
        'Date of Contribution: ',
        default=datetime.now)
    maf_ref=models.CharField(
        max_length=99,
        null=False,
        default="forwarded balance")
    maf_debit=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])
    maf_credit=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])
    maf_total=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=10,
        decimal_places=2,
        # validators=[MinValueValidator(0.01)]
    )

    # def __unicode__(self):
    #     return u'%s' % (self.maf_total)


class ODF(models.Model):
    odf_client=models.ForeignKey(Client)
    # maf_beneficiary=models.ForeignKey(Client.beneficiary)
    odf_id=models.AutoField(primary_key=True)
    odf_contrib_date=models.DateField(
        'Date of Contribution: ',
        default=datetime.now)
    odf_ref=models.CharField(
        max_length=99,
        null=False,
        default="forwarded balance")
    odf_debit=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])
    odf_credit=models.DecimalField(
        null=True,
        default="-",
        blank=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])
    odf_total=models.DecimalField(
        null=True,
        default="",
        blank=True,
        max_digits=10,
        decimal_places=2,
        # validators=[MinValueValidator(0.01)]
    )