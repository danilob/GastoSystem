from django.shortcuts import render

from expenses.forms import SelectCategoryForm
from expenses.models import *

from django.db.models import Sum

def list_expenses_by_category(request):
  if request.method == 'POST':
    form = SelectCategoryForm(request.POST)
    if form.is_valid():
      category = form.cleaned_data['category']
      list = Expense.objects.filter(category=category).values('date__year','date__month').annotate(total=Sum('value')).order_by('-date__year','-date__month')
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