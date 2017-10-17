"""Create your tasks here"""

# updates the interest per month of
# basis: monthly dimishing balance

from __future__ import absolute_import, unicode_literals
from celery import Celery, shared_task, task
from celery.decorators import task, periodic_task
from celery.task.schedules import crontab
from clients.models import Loan
from django.core.management import call_command
from django.shortcuts import redirect
from vamps import views
import datetime

app = Celery()


@periodic_task(run_every=(crontab(minute='*/1')), name="prr", ignore_result=True)
def prr():
	print "hello"
	return 1


# @periodic_task(run_every=(crontab(0 0 * * *)), name="dailyUp")
@periodic_task(run_every=(crontab(minute='*/1')), name="dailyUp", ignore_result=True)
def dailyUp():
	"""checks for updates everyday at midnight"""
	loan_id = Loan.objects.filter(loan_status="Outstanding") #queryset of all outstanding loans
	for index in xrange(len(loan_id)):
		loanApp_id = loan_id[index].loan_application.approval_date
		loanDur = loan_id[index].loan_duration
		# print loanApp_id
		xp = views.compute_dur(loanApp_id, loanDur)
		# print xp
		if datetime.datetime.today().date() <= xp and loanApp_id != datetime.datetime.today().date():
			if datetime.datetime.today().date().day == loanApp_id.day:
				print "update"
				loan_id[index].update = True
				loan_id[index].save()
			else:
				print "no update"
		elif datetime.datetime.today().date() <= xp and loanApp_id == datetime.datetime.today().date():
			print "applied just today"
		else:
			loan_id[index].overdue = True
			print "overdue"
	return 0


# @periodic_task(run_every=(crontab(0 0 * * *)), name="dailyBackUp")
def dailyBackUp():
	"""backs up the database to another location at midnight"""
	# edit path
	with open('C:\\Users\\yaranon family\\Desktop\\sample.bak', 'w') as f:
		call_command('dumpdata', 'clients', indent=3, exclude=['contenttypes', 'auth'], use_natural_foreign_keys=True, stdout=f)
	return 0

