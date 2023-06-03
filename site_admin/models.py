from django.db import models
from account.models import Account


class Bank(models.Model):
    name = models.CharField(max_length=150)
    date_added = models.DateTimeField(auto_now_add=True)


class Support(models.Model):
    subject = models.CharField(max_length=50, blank=True, null=True)
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    ticket_id = models.CharField(max_length=15)
    topic = models.CharField(max_length=60)
    mobile = models.CharField(max_length=25)
    date_created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=2000)
    status = models.CharField(max_length=25, default='open')
