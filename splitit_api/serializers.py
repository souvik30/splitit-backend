from rest_framework import serializers
from models import Users, ExpenseGroups, Expenses, Spenders, Borrowers, GroupMemberships


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'email']


class ExpenseGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseGroups
        fields = ['id', 'name', 'description', 'force_settled', 'owner']


class GroupMembershipsGetSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = GroupMemberships
        fields = ['id', 'user_id', 'user_name', 'user_email', 'group']


class ExpenseGroupsGetSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    members = serializers.SerializerMethodField()

    def get_members(self, obj):
        members_qs = GroupMemberships.objects.filter(group=obj)
        return GroupMembershipsGetSerializer(members_qs, many=True).data

    class Meta:
        model = ExpenseGroups
        fields = ['id', 'name', 'description', 'owner_name', 'owner_email', 'members']


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ['id', 'group', 'name', 'description', 'date', 'owner', 'type']


class ExpensesGetSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)

    class Meta:
        model = Expenses
        fields = ['id', 'group', 'name', 'description', 'date', 'owner_name', 'type']


class SpendersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spenders
        fields = '__all__'


class BorrowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowers
        fields = '__all__'
