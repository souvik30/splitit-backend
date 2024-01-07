from .models import Spenders, Borrowers


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
