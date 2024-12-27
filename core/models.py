from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils import timezone


class CustomUser(AbstractUser):
    ACCOUNT_TYPES = (
        ('administrator', 'Administrator'),
        ('regular', 'Regular User'),
    )
    email = models.EmailField(unique=True)  # Enforce uniqueness for email
    account_type = models.CharField(max_length=15, choices=ACCOUNT_TYPES)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def is_admin(self):
        return self.account_type == 'administrator'

    def can_borrow(self):
        return self.account_type == 'regular' and self.lendings.filter(is_returned=False).count() < 5



class LibraryItem(models.Model):
    name = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    identifier = models.CharField(max_length=13, unique=True, null=True, blank=True)
    total_stock = models.PositiveIntegerField()
    available_stock = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='added_books')

    def check_availability(self):
        return self.available_stock > 0

    def lend_item(self):
        if self.check_availability():
            self.available_stock -= 1
            self.save()

    def return_item(self):
        self.available_stock += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:  # Initialize available stock on first save
            self.available_stock = self.total_stock
        super().save(*args, **kwargs)


class LendingRecord(models.Model):
    borrower = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='lendings')
    item = models.ForeignKey('LibraryItem', on_delete=models.CASCADE, related_name='lending_records')
    date_borrowed = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_returned = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)
        super().save(*args, **kwargs)


class ReturnTransaction(models.Model):
    lending_record = models.OneToOneField('LendingRecord', on_delete=models.CASCADE, related_name='return_transaction')
    date_returned = models.DateTimeField(auto_now_add=True)
    penalty_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def compute_penalty(self):
        if timezone.is_naive(self.lending_record.due_date):
            self.lending_record.due_date = timezone.make_aware(self.lending_record.due_date)

        if self.lending_record.due_date < timezone.now():
            days_late = (timezone.now() - self.lending_record.due_date).days
            return days_late * 5  # Penalty rate of 5 BDT per day
        return 0.0


class Penalty(models.Model):
    lending_record = models.OneToOneField('LendingRecord', on_delete=models.CASCADE, related_name='penalty')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    lending_record = models.ForeignKey('LendingRecord', on_delete=models.CASCADE, related_name='payments')
    penalty = models.ForeignKey('Penalty', on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount_settled = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)