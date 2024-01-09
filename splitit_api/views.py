from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import Users, ExpenseGroups, Expenses, GroupMemberships
from . import serializers
from .exceptions import InvalidAuthToken
from .authentication import get_firebase_uid, get_firebase_user, FirebaseAuthentication
from drf_yasg.utils import swagger_auto_schema
from .schema import schemas
from itertools import combinations
from .utils import calculate_borrowers_amount, create_expense_with_spenders_and_borrowers


class AuthViewSet(APIView):
    permission_classes = []
    authentication_classes = []

    @swagger_auto_schema(request_body=schemas.AuthRequestSchema(),
                         responses={200: serializers.UsersSerializer()})
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

    @action(methods=['get'], detail=False, url_path='email')
    @swagger_auto_schema(responses={200: serializers.UsersSerializer()},
                         manual_parameters=[
                             schemas.email_query_param,
                         ])
    def get_user_by_email(self, request):
        email = request.query_params.get('email')
        user = Users.objects.get(email=email)
        return Response(data=serializers.UsersSerializer(user).data, status=HTTP_200_OK)


@swagger_auto_schema(query_serializer=serializers.ExpenseGroupsGetSerializer(),
                     responses={200: serializers.ExpenseGroupsSerializer()})
class ExpenseGroupsViewSet(viewsets.ModelViewSet):
    queryset = ExpenseGroups.objects.all()
    serializer_class = serializers.ExpenseGroupsGetSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def get_queryset(self):
        owner = self.request.user
        memberships = GroupMemberships.objects.filter(user=owner)
        group_ids = [membership.group.pk for membership in memberships]
        groups = ExpenseGroups.objects.filter(pk__in=group_ids)
        return groups

    def create(self, request, *args, **kwargs):
        owner = self.request.user
        request.data['owner'] = owner.pk
        serializer = serializers.ExpenseGroupsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # Now create a group membership
        GroupMemberships.objects.create(
            group=instance,
            user=owner
        )
        return Response(
            data=self.serializer_class(instance).data,
            status=HTTP_200_OK
        )



    @action(methods=['post'], detail=True, url_path='add_user')
    @swagger_auto_schema(request_body=schemas.AddUserToGroupRequestSchema(),
                         responses={200: schemas.MessageResponseSchema()})
    def add_user(self, request, pk=None):
        user_id = request.data.get('user_id')
        user = Users.objects.get(id=user_id)
        print(int(pk))
        GroupMemberships.objects.create(
            group=self.get_object(),
            user=user
        )
        return Response(data={"message": "Added user to group"}, status=HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='expenses')
    @swagger_auto_schema(responses={200: serializers.ExpensesGetSerializer(many=True)})
    def expenses(self, request, pk=None):
        expense_group = self.get_object()
        expenses_for_group = Expenses.objects.filter(group=expense_group)

        return Response(
            data=serializers.ExpensesGetSerializer(expenses_for_group, many=True).data,
            status=HTTP_200_OK
        )

    @action(methods=['get'], detail=True, url_path='balances')
    @swagger_auto_schema(responses={200: schemas.GetBalancesResponseSchema()})
    def balances(self, request, pk=None):
        expense_group = self.get_object()
        group_members = GroupMemberships.objects.filter(group=expense_group)
        users_list = [member.user.id for member in group_members]
        user_pairs = list(combinations(users_list, 2))
        response = []
        for pair in user_pairs:
            # calculate user A -> B
            user1, user2 = pair
            user_2_borrowed_amount = calculate_borrowers_amount(user1, user2, users_list)

            user_1_borrowed_amount = calculate_borrowers_amount(user2, user1, users_list)

            if user_1_borrowed_amount > 0 or user_2_borrowed_amount > 0:

                if user_1_borrowed_amount > user_2_borrowed_amount:
                    response.append({
                        "spender": user2,
                        "borrower": user1,
                        "amount": user_1_borrowed_amount - user_2_borrowed_amount
                    })
                else:
                    response.append({
                        "spender": user1,
                        "borrower": user2,
                        "amount": user_2_borrowed_amount - user_1_borrowed_amount
                    })

        return Response(
            data=response,
            status=HTTP_200_OK
        )


@swagger_auto_schema(query_serializer=serializers.ExpensesGetSerializer(),
                     responses={200: serializers.ExpensesGetSerializer()})
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = serializers.ExpensesGetSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    @swagger_auto_schema(request_body=schemas.ExpenseCreateSchema(),
                         responses={200: serializers.ExpensesGetSerializer()})
    def create(self, request, *args, **kwargs):
        owner = self.request.user
        data = request.data
        data['owner'] = owner

        expense = create_expense_with_spenders_and_borrowers(data)

        return Response(data=self.serializer_class(expense).data,
                        status=HTTP_200_OK)
