from django.db import models

# Create your models here.
from django.db import models


class Users(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)


class ExpenseGroups(models.Model):
    name = models.CharField(max_length=1000, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    force_settled = models.BooleanField(default=False)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class GroupMemberships(models.Model):
    group = models.ForeignKey(ExpenseGroups, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Expenses(models.Model):
    class ExpenseTypes(models.TextChoices):
        EXPENSE = 'EXPENSE', 'Expense'
        SETTLEMENT = 'SETTLEMENT', 'Settlement'

    group = models.ForeignKey(ExpenseGroups, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    type = models.CharField(choices=ExpenseTypes.choices,
                            null=False, blank=False, max_length=10)


class Spenders(models.Model):
    expense = models.ForeignKey(Expenses, on_delete=models.CASCADE)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=3)


class Borrowers(models.Model):
    expense = models.ForeignKey(Expenses, on_delete=models.CASCADE)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=3)

