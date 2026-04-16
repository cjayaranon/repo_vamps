from celery import shared_task
from django.core.management import call_command
from clients.models import Loan
from vamps import views
import datetime


@shared_task(name="prr", ignore_result=True)
def prr():
    print("hello")
    return 1


@shared_task(name="dailyUp", ignore_result=True)
def daily_up():
    """Checks for loan updates."""
    today = datetime.date.today()
    loans = Loan.objects.filter(loan_status="Outstanding")

    for loan in loans:
        loan_app_date = loan.loan_application.approval_date
        loan_duration = loan.loan_duration
        expiry_date = views.compute_dur(loan_app_date, loan_duration)

        if today <= expiry_date and loan_app_date != today:
            if today.day == loan_app_date.day:
                loan.update = True
                loan.save(update_fields=["update"])
            else:
                print("no update")
        elif today <= expiry_date and loan_app_date == today:
            print("applied just today")
        else:
            loan.overdue = True
            loan.save(update_fields=["overdue"])

    return 0


@shared_task(name="dailyBackUp", ignore_result=True)
def daily_backup():
    """Backs up the database to another location."""
    with open(r"C:\Users\yaranon family\Desktop\sample.bak", "w") as f:
        call_command(
            "dumpdata",
            "clients",
            indent=3,
            exclude=["contenttypes", "auth"],
            use_natural_foreign_keys=True,
            stdout=f,
        )
    return 0