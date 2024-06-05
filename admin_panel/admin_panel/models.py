from django.db import models


class User(models.Model):
    record_id = models.AutoField(primary_key=True, blank=False, unique=True)
    user_name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return f"{self.user_name}"


class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    type_transaction = models.CharField(max_length=100, blank=False, null=False)
    amount = models.FloatField(blank=False, null=False)

    class Meta:
        db_table = "transactions"
        verbose_name_plural = 'Транзакції'


