from django.urls import path

from expenses.views import *

app_name = 'expenses'

urlpatterns = [
    path('get/report/list-expenses-by-category/', list_expenses_by_category, name="list_expenses_by_category"),


    
]