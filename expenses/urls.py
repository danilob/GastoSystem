from django.urls import path

from expenses.views import *

app_name = 'expenses'

urlpatterns = [
    path('', home,name="home"),
    path('page/<int:page>', home,name="home"),
    path('report/', report, name="report"),
    path('about/', about, name="about"),

    path('get-total-expenses/',get_total_expenses_ajax,name="get_total_expenses_ajax"),


    #gerenciamento de modais
    path('new/expense/', create_expense, name="create_expense"),
    path('handle/limit', handle_limit, name="handle_limit"),
    path('handle/payment', handle_payment, name="handle_payment"),
    path('handle/category', handle_category, name="handle_category"),
    path('edit/expense',edit_expense,name="edit_expense"),
    path('delete/expense/<int:id>',delete_expense,name="delete_expense"),

    #relatórios
    path('get/report/list-expenses-by-category/', list_expenses_by_category, name="list_expenses_by_category"),
    path('get/report/get-bigger-expenses-by-category/', list_expenses_by_category_top, name="list_expenses_by_category_top"),
    path('get/report/list-expenses-by-period/', list_expenses_by_period, name="list_expenses_by_period"),
    path('get/report/list-category-by-period/', list_category_by_period, name="list_category_by_period"),
    path('get/report/sum-expenses-by-payment-and-period/', sum_expenses_payment_and_period, name="sum_expenses_payment_and_period"),
    path('get/report/list-total-expense-and-limit/', list_total_expenses_and_limit, name="list_total_expenses_and_limit"),

]