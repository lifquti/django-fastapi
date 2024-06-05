from django.contrib import admin
from .models import User, Transactions


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'user_name')


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_id', 'amount')
