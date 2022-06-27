from unicodedata import category
from django.test import TestCase

from expenses.models import Category, Limit
from django.core.exceptions import ValidationError

class TestLimit(TestCase):

    def setUp(self):
        pass

    def test_check_creation_limit_invalid_month(self):
        limit = Limit(
                year = 2022,
                month = 13,
                value = 1000
            )
        self.assertRaises(ValidationError,
            lambda: limit.save()
        )

        limit = Limit(
                year = 2022,
                month = 0,
                value = 1000
            )
        self.assertRaises(ValidationError,
            lambda: limit.save()
        )

    def test_check_value_limit_negative(self):
        limit = Limit(
                year = 2022,
                month = 8,
                value = -1000
            )
        self.assertRaises(ValidationError,
            lambda: limit.save()
        )

from expenses.models import Expense, Category, Payment
from datetime import datetime

class TestExpenses(TestCase):

    def setUp(self):
        self.category1 = Category.objects.create(description='Combustível')
        self.payment1 = Payment.objects.create(description='Pix')
        
    def test_check_value_limit_negative(self):
        expense = Expense(
                category = self.category1, payment=self.payment1,
                date = datetime(2022, 1, 13).date(),
                value = -1000,description="Gasto"
            )
        self.assertRaises(ValidationError,lambda: expense.save())


    def test_list_expenses_by_category(self):
        cat_1 = Category.objects.create(description="Lanche")
        cat_2 = Category.objects.create(description="Supermercado")
        pay_1 = Payment.objects.create(description="Débito")

        expense_1 = Expense.objects.create(category=cat_1,payment=pay_1,
                date = datetime(2022, 5, 25).date(),
                value = 5, description="Lanche UESPI"
            )
        expense_2 = Expense.objects.create(category=cat_1,payment=pay_1,
                date = datetime(2022, 5, 15).date(),
                value = 15, description="Lanche Feira"
            )
        expense_3 = Expense(category=cat_1,payment=pay_1,
                date = datetime(2022, 5, 12).date(),
                value = 25, description="Lanche padaria"
            )
        expense_4 = Expense.objects.create(category=cat_2,payment=pay_1,
                date = datetime(2022, 5, 12).date(),
                value = 25, description="Compras semanal"
            )
        expense_5 = Expense.objects.create(category=cat_1,payment=pay_1,
                date = datetime(2022, 6, 22).date(),
                value = 15, description="Lanche UESPI"
            )
        expense_6 = Expense.objects.create(category=cat_1,payment=pay_1,
                date = datetime(2022, 6, 22).date(),
                value = 7, description="Lanche padaria"
            )
        expense_7 = Expense.objects.create(category=cat_1,payment=pay_1,
                date = datetime(2022, 4, 30).date(),
                value = 17, description="Lanche padaria"
            )
        result_expected = [
            {
                'date__year': 2022, 
                'date__month': 6, 
                'total': 22
            },
            {
                'date__year': 2022, 
                'date__month': 5, 
                'total': 20
            },
            {
                'date__year': 2022, 
                'date__month': 4, 
                'total': 17
            },
        ]
        self.assertQuerysetEqual(Expense.list_expenses_by_category(cat_1),result_expected)