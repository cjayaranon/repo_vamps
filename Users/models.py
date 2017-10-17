from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):

    
    ADMIN='Admin'
    BOOKKEEPER='Bookkeeper'
    CASHIER='Cashier'

    POS = (
        (ADMIN, 'Admin'),
        (BOOKKEEPER, 'Bookkeeper'),
        (CASHIER, 'Cashier'),
    )
    position = models.CharField(
        choices=POS,
        default=ADMIN,
        max_length=10,
    )

    # userpic = models.ImageField()

    # def __unicode__(self):
    #     return self.username