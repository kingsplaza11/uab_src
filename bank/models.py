from email.policy import default
from django.db import models
from account.models import Account
from utils.unique_generators import GenerateUUIDCode


class BankAccount(models.Model):
    user = models.OneToOneField(Account, related_name='bank_account', on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    bank = models.CharField(max_length=150, default='uab')
    account_number = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    transfer_pin = models.CharField(max_length=4, blank=True, null=True, default='----')
    blocked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user} - {self.account_number} - {self.balance}'

    def save(self, *args, **kwargs):
        self.balance = round(self.balance, 3)
        Acc_No = self.generate_account_number()
        account_no_available = BankAccount.objects.filter(account_number=Acc_No).exists()

        while account_no_available:
            Acc_No = self.generate_account_number()
            account_no_available = BankAccount.objects.filter(account_number=Acc_No).exists()
        else:
            self.account_number = Acc_No
        super().save(*args, **kwargs)

    def generate_account_number(self):
        new_account_no = '27' + GenerateUUIDCode.numeric_uid(8)
        return new_account_no


class Deposit(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='deposits')
    amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=12)
    status = models.CharField(max_length=25)
    method = models.CharField(max_length=50)
    description = models.CharField(max_length=500)


class Withdrawal(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=12)
    status = models.CharField(max_length=25)
    method = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 3)
        super().save( *args, **kwargs)



class Transfer(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers')
    amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=12)
    status = models.CharField(max_length=25)
    trf_from = models.CharField(max_length=50)
    trf_to = models.CharField(max_length=50)


class History(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='history')
    amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20)