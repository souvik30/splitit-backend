from .models import Spenders, Borrowers, Expenses, ExpenseGroups, Users
from django.db import transaction


def calculate_borrowers_amount(spender_id, borrower_id, expense_group):
    spendings = Spenders.objects.filter(owner=spender_id, expense__group=expense_group)
    amount = 0.0
    for spending in spendings:
        expense = spending.expense
        borrower = Borrowers.objects.filter(owner=borrower_id, expense=expense)
        if borrower.exists():
            borrower = borrower[0]
            amount += borrower.amount

    return amount


@transaction.atomic
def create_expense_with_spenders_and_borrowers(request_data):
    try:
        # Assuming you have Expense, Spender, and Borrower models defined
        expense_group = ExpenseGroups.objects.get(id=int(request_data['group']))
        # Create the Expense object
        expense = Expenses.objects.create(
            group=expense_group,
            name=request_data['name'],
            description=request_data['description'],
            type=request_data['type'],
            owner=request_data['owner']
        )

        spenders_data = request_data.get('spenders', [])
        borrowers_data = request_data.get('borrowers', [])

        # Create spenders for the expense
        for spender_info in spenders_data:
            spender_owner = Users.objects.get(id=spender_info['owner'])
            Spenders.objects.create(
                amount=spender_info['amount'],
                owner=spender_owner,
                expense=expense
            )

        # Create borrowers for the expense
        for borrower_info in borrowers_data:
            borrower_owner = Users.objects.get(id=borrower_info['owner'])
            Borrowers.objects.create(
                amount=borrower_info['amount'],
                owner=borrower_owner,
                expense=expense
            )
        return expense

    except Exception as e:
        # If any exception occurs during creation, rollback the transaction
        transaction.set_rollback(True)
        # Handle the exception, log, or raise it as needed
        raise e
