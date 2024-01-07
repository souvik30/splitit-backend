from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView
from .models import Users, ExpenseGroups, Expenses
from . import serializers
from .exceptions import InvalidAuthToken
from .authentication import get_firebase_uid, FirebaseAuthentication, get_firebase_user


class AuthViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        id_token = request.data.get('idToken')
        firebase_uid = get_firebase_uid(id_token)
        if firebase_uid is None:
            raise InvalidAuthToken('Invalid auth token')

        # Check if user exists in our db
        try:
            user = Users.objects.get(id=firebase_uid)
        except Users.DoesNotExist:
            # Create the user record
            user_info = get_firebase_user(firebase_uid)
            user_szs = serializers.UsersSerializer(data=user_info)
            if user_szs.is_valid():
                user_szs.save()
            user = Users.objects.get(id=firebase_uid)

        return Response(data=serializers.UsersSerializer(user).data, status=HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = serializers.UsersSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST /user is not allowed")


class ExpenseGroupsViewSet(viewsets.ModelViewSet):
    queryset = ExpenseGroups.objects.all()
    serializer_class = serializers.ExpenseGroupsGetSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = serializers.ExpensesSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
