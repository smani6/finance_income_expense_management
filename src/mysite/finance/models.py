from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Account_id = models.CharField(max_length=100)


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    created_by = models.CharField(max_length=200, null=True)
    created_datetime = models.DateTimeField(null=True)
    modified_by = models.CharField(max_length=200, null=True)
    modified_datetime = models.DateTimeField(null=True)


class IncomeInfo(models.Model):
    account_id = models.ForeignKey(Account)
    trans_subtype = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    tag = models.CharField(max_length=200)
    date = models.DateField()
    created_by = models.CharField(max_length=200, null=True)
    created_datetime = models.DateTimeField(null=True)
    modified_by = models.CharField(max_length=200, null=True)
    modified_datetime = models.DateTimeField(null=True)


class ExpenseInfo(models.Model):
    account_id = models.ForeignKey(Account)
    trans_subtype = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    tag = models.CharField(max_length=200)
    date = models.DateField()
    created_by = models.CharField(max_length=200, null=True)
    created_datetime = models.DateTimeField(null=True)
    modified_by = models.CharField(max_length=200, null=True)
    modified_datetime = models.DateTimeField(null=True)
