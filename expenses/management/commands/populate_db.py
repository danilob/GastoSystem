from unicodedata import category
from django.core.management.base import BaseCommand
from tqdm import tqdm

from datetime import datetime
from datetime import timedelta
import random

from expenses.models import Expense, Payment, Category, Limit


#https://factoryboy.readthedocs.io/en/stable/index.html
import factory
import factory.fuzzy
from faker import Faker


class _ExpenseFactoryBoy(factory.django.DjangoModelFactory):
    """Using factoryboy and faker to create test factory"""
    class Meta:
        model = 'Expense'
    
    category = factory.LazyFunction(lambda: random.choice(Category.objects.all())[0])
    payment = factory.LazyFunction(lambda: random.choice(Payment.objects.all())[0])
    value = factory.fuzzy.FuzzyFloat(0.1, 7500).fuzz()
    description = Faker().sentence()
    date = factory.Faker('date_between',
                               start_date='-4y',
                               end_date=datetime(year=2021, month=12, day=31))


class UserFactory:
    """Object to create User for testing purposes"""

    @classmethod
    def create_valid_instance(cls, **kwargs):
        return _ExpenseFactoryBoy.create(**kwargs)



class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _delete_database(self):
        Expense.objects.all().delete()
        Category.objects.all().delete()
        Payment.objects.all().delete()
        Limit.objects.all().delete()
        

    def _create_database(self):
        print("Creating categories")
        with tqdm(total=10) as pbar:
            Category.objects.create(description="Lanche")
            pbar.update(1)
            Category.objects.create(description="Supermercado")
            pbar.update(1)
            Category.objects.create(description="Energia")
            pbar.update(1)
            Category.objects.create(description="Refeição")
            pbar.update(1)
            Category.objects.create(description="Combustível")
            pbar.update(1)
            Category.objects.create(description="Conserto")
            pbar.update(1)
            Category.objects.create(description="Roupas")
            pbar.update(1)
            Category.objects.create(description="Água")
            pbar.update(1)
            Category.objects.create(description="Curso")
            pbar.update(1)
            Category.objects.create(description="Viagem")
            pbar.update(1)
        
        print("Creating payments")
        with tqdm(total=6) as pbar:
            Payment.objects.create(description="Pix")
            pbar.update(1)
            Payment.objects.create(description="Dinheiro")
            pbar.update(1)
            Payment.objects.create(description="Nubank C")
            pbar.update(1)
            Payment.objects.create(description="Nubank D")
            pbar.update(1)
            Payment.objects.create(description="Visa D")
            pbar.update(1)
            Payment.objects.create(description="Visa C")
            pbar.update(1)

        print("Creating limits")
        from tqdm import trange
        for i in trange(4*12):
            while True:
                month = factory.fuzzy.FuzzyInteger(low=1, high=12,step=1).fuzz()
                year = factory.fuzzy.FuzzyInteger(low=2018, high=2021,step=1).fuzz()
                if(not Limit.objects.filter(month=month, year=year).exists()):
                    value = factory.fuzzy.FuzzyFloat(1000, 2500).fuzz()
                    Limit.objects.create(month=month,year=year,value=value)
                    break
        print("Creating expenses")
        from random import choice
        for i in trange(500):
            
           
            while True:
                try:
                    pks = Category.objects.values_list('pk', flat=True)
                    random_pk = choice(pks)
                    category = Category.objects.get(pk=random_pk)
                    pks = Payment.objects.values_list('pk', flat=True)
                    random_pk = choice(pks)
                    payment = Payment.objects.get(pk=random_pk)
                    value = factory.fuzzy.FuzzyInteger(1, 500).fuzz()
                    description = f'{Faker().sentence()}'
                    date = Faker().date_between_dates(datetime(year=2018, month=1, day=1),datetime(year=2021, month=12, day=31))
                    Expense.objects.create(category=category,payment=payment,value=value,description=description,date=date)
                    break
                except Exception as e:
                    print(e)
                    
        
    def handle(self, *args, **options):
        print("Delete expenses, categories, payments and limits")
        self._delete_database()
        self._create_database()