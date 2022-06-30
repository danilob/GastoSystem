from django.shortcuts import render

from expenses.forms import SelectCategoryForm
from expenses.models import *


def list_expenses_by_category(request):
  if request.method == 'POST':
    form = SelectCategoryForm(request.POST)
    if form.is_valid():
      category = form.cleaned_data['category']
      list = Expense.list_expenses_by_category(category)
      context = {
        'form': form,
        'category_selected': category,
        'list':list
      }
      return render(request,'expenses/list-expenses-by-category.html',context)
  form = SelectCategoryForm()
  context = {
    'form': form,
  }
  return render(request,'expenses/list-expenses-by-category.html',context)