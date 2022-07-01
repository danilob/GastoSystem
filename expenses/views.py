from django.shortcuts import render

from expenses.forms import SelectCategoryForm
from expenses.models import *


def home(request):
  # context = {
  #    'page_selected': "home",
  # }
  # return render(request,"expenses/main.html", context)
  return render(request,"base.html", context={})

def about(request):
  context = {
     'page_selected': "about",
  }
  return render(request,"expenses/about.html", context)

def report(request):
  context = {
     'page_selected': "report",
  }
  return render(request,"expenses/report.html", context)



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