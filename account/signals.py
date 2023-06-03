from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from bank.models import BankAccount


user = settings.AUTH_USER_MODEL

@receiver(post_save, sender=user)
def create_bank_account(sender, instance, created, **kwargs):
    if created:
        BankAccount.objects.create(user=instance)


