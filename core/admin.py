# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'account_type', 'is_staff', 'is_active')
    list_filter = ('account_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('account_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('account_type',)}),
    )


@admin.register(LibraryItem)
class LibraryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'writer', 'identifier', 'total_stock', 'available_stock', 'date_added', 'last_modified', 'added_by')
    list_filter = ('writer', 'date_added', 'last_modified')
    search_fields = ('name', 'writer', 'identifier')
    ordering = ('name',)


@admin.register(LendingRecord)
class LendingRecordAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'item', 'date_borrowed', 'due_date', 'is_returned', 'created_on', 'updated_on')
    list_filter = ('is_returned', 'date_borrowed', 'due_date')
    search_fields = ('borrower__username', 'item__name')
    ordering = ('-date_borrowed',)


@admin.register(ReturnTransaction)
class ReturnTransactionAdmin(admin.ModelAdmin):
    list_display = ('lending_record', 'date_returned', 'penalty_paid', 'created_on', 'updated_on')
    list_filter = ('date_returned', 'penalty_paid')
    search_fields = ('lending_record__borrower__username', 'lending_record__item__name')
    ordering = ('-date_returned',)


@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('lending_record', 'amount', 'is_paid', 'created_on', 'updated_on')
    list_filter = ('is_paid',)
    search_fields = ('lending_record__borrower__username', 'lending_record__item__name')
    ordering = ('-created_on',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('lending_record', 'penalty', 'payment_date', 'amount_settled', 'created_on', 'updated_on')
    list_filter = ('payment_date',)
    search_fields = ('lending_record__borrower__username', 'lending_record__item__name')
    ordering = ('-payment_date',)
