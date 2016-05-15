from django.db import models

# Create your models here.

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    
class IncomeInfo(models.Model):
    account_id = models.ForeignKey(Account)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    tag = models.CharField(max_length=200)
    date = models.DateField()
    
class ExpenseInfo(models.Model):
    account_id = models.ForeignKey(Account)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    tag = models.CharField(max_length=200)
    date = models.DateField()