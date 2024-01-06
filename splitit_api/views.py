from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Users, ExpenseGroups, Expenses
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = serializers.UsersSerializer
    permission_classes = []


class ExpenseGroupsViewSet(viewsets.ModelViewSet):
    queryset = ExpenseGroups.objects.all()
    serializer_class = serializers.ExpenseGroupsGetSerializer()
    permission_classes = []


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = serializers.ExpensesSerializer()
    permission_classes = []