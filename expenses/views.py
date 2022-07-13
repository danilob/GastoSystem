from multiprocessing import context
from django.shortcuts import render,redirect
from django.urls import reverse

from expenses.forms import SelectCategoryForm
from expenses.models import *

from datetime import datetime
from django.db.models import Sum
import math 
NUMBER_ITENS = 6

def get_month_by_number(month):
  dict_month = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro",
  }
  return dict_month[month]


def build_list_month_year(start_date, end_date):
  diff_month = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
  diff_month += 1
  month_init = start_date.month
  year_init = start_date.year
  list_month_year = []
  for i in range(diff_month):
    if(month_init>12):
      month_init = 1
      year_init += 1
    list_month_year.append(
      {
        'month':get_month_by_number(month_init),
        'year':year_init,
        'month_number':month_init,
      }
    )
    month_init += 1
  list_month_year.reverse()
  return list_month_year

def home(request,page=None):
  global NUMBER_ITENS
  today = datetime.now()
  current_month = today.month
  current_year = today.year
  total_current_month = Expense.objects.filter(date__month=current_month,date__year=current_year).aggregate(total=Sum('value'))
  expense_first = Expense.objects.all().order_by('date').first()
  date_begin = expense_first.date if expense_first else today
  list_month_year_select = build_list_month_year(date_begin,today)
  count_expenses = Expense.objects.all().count()
  current_page = 1
  if page or page==0:
    current_page = page
  elif request.session.get('session_page', False):
    current_page = request.session.get('session_page')

  num_pages = math.ceil(count_expenses/NUMBER_ITENS)
  if num_pages:
    if(current_page>num_pages):
      return redirect(reverse('expenses:home', kwargs={'page': num_pages}))
    if (current_page<1):
      return redirect(reverse('expenses:home', kwargs={'page': 1}))
    request.session['session_page'] = current_page

  

  list_item_expenses = []
  if (num_pages == current_page) and Expense.objects.all().exists():
    list_item_expenses = Expense.objects.all()[NUMBER_ITENS*(current_page-1):]
  elif Expense.objects.all().exists():
    list_item_expenses = Expense.objects.all()[NUMBER_ITENS*(current_page-1):NUMBER_ITENS*current_page-1]

  # if(count_expenses>=NUMBER_ITENS):
  #   list_item_expenses = Expense.objects.all()[:NUMBER_ITENS]
  # else:
  #   list_item_expenses = Expense.objects.all()
  
  context = {
     'page_selected': "home",
     'total_current_month': total_current_month['total'],
     'current_month_number': current_month,
     'current_month': get_month_by_number(current_month),
     'current_year': current_year,
     'list_month_year_select': list_month_year_select,
     'list_item_expenses': list_item_expenses,
     'num_pages': num_pages,
     'current_page': current_page

  }
  return render(request,"expenses/main.html", context)
  # return render(request,"base.html", context={})

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


from django.http import JsonResponse
def get_total_expenses_ajax(request):
  if (request.method == 'GET'):
    values = request.GET['value'].split('-')
    month_selected = values[0]
    year_selected = values[1]
    total = Expense.objects.filter(date__month=month_selected,date__year=year_selected).aggregate(total=Sum('value'))
    print('TOTAL', total)
    total_expenses = total['total'] if ('total' in total) else 0
    percent = '??'
    if Limit.objects.filter(month=month_selected,year=year_selected).exists():
      limit = Limit.objects.get(month=month_selected,year=year_selected).value
      try:
        percent = int(100*total_expenses/limit)
      except:
        percent = 0
    response = {
      'data':total_expenses,
      'percent':f'{percent} %'
    }

  return JsonResponse(response, status = 200)

from expenses.forms import ExpenseForm
from django.template.loader import render_to_string

def create_expense(request):
  title = 'Inserir Gasto'
  context_extra = {}
  if request.POST.get('action') == 'post':
    form = ExpenseForm(request.POST)
    
    if form.is_valid():
      model = form.save(commit=False)
      model.save()
      context_extra = {
          'response' : 'Criado com sucesso!',
          'error': False,
      }
    else:
      context_extra = {
          'response' : 'Erros ocorreram!',
          'error': True
      }
   
  else:
        form = ExpenseForm()
  context = {
    'form': form,
  }
  html_page = render_to_string('expenses/form/new-expense.html', context)
  response = {
    'title' : title,
    'html' : html_page,
    'response' : context_extra['response'] if 'response' in context_extra else None,
    'error': context_extra['error'] if 'error' in context_extra else None,
  }
  return JsonResponse(response, status = 200)

from expenses.forms import CategoryForm

def handle_category(request):
  title = "Inserir Categoria"
  context_extra = {}
  if request.POST.get('action') == 'post':
    form = CategoryForm(request.POST)
    
    if form.is_valid():
      model = form.save(commit=False)
      model.save()
      context_extra = {
          'response' : 'Criado com sucesso!',
          'error': False,
      }
    else:
      context_extra = {
          'response' : 'Erros ocorreram!',
          'error': True
      }
   
  else:
        form = CategoryForm()
        if 'action' in request.GET and request.GET['action'] == 'delete':
          item = request.GET['id_delete']
          category = Category.objects.get(description__iexact=item)
          category.delete()
  context = {
    'form': form,
    'categories': Category.objects.all()
  }
  html_page = render_to_string('expenses/form/new-category.html', context)
  response = {
    'title' : title,
    'html' : html_page,
    'response' : context_extra['response'] if 'response' in context_extra else None,
    'error': context_extra['error'] if 'error' in context_extra else None,
  }
  return JsonResponse(response, status = 200)

from expenses.forms import LimitForm
from expenses.models import Limit
def handle_limit(request):
  title = 'Inserir Limite'

  
  context_extra = {}
  if request.POST.get('action') == 'post':
    
    month, year = request.POST['month'], request.POST['year']
 
    if Limit.objects.filter(month=month,year=year).exists():
      instance = Limit.objects.get(month=month,year=year)
      form = LimitForm(request.POST,instance=instance)
    else:
      form = LimitForm(request.POST)
    
    if form.is_valid():
      model = form.save(commit=False)
      model.save()
      context_extra = {
          'response' : 'Criado com sucesso!',
          'error': False,
      }
    else:
      context_extra = {
          'response' : 'Erros ocorreram!',
          'error': True,
      }
   
  else:
    value = request.GET['month_year']
    value = value.split('-')
    month, year = value[0], value[1]
    total = 0
    if Limit.objects.filter(month=month,year=year).exists():
      total = Limit.objects.get(month=month,year=year).value
    form = LimitForm(initial={'month': month, 'year': year, 'value': total})
  context = {
    'form': form,
  
  }
  html_page = render_to_string('expenses/form/handle-limit.html', context)
  response = {
    'title' : title,
    'html' : html_page,
    'response' : context_extra['response'] if 'response' in context_extra else None,
    'error': context_extra['error'] if 'error' in context_extra else None,
  }
  return JsonResponse(response, status = 200)

from expenses.forms import PaymentForm

def handle_payment(request):
  title = "Inserir Forma de Pagamento"
  context_extra = {}
  if request.POST.get('action') == 'post':
    form = PaymentForm(request.POST)
    
    if form.is_valid():
      model = form.save(commit=False)
      model.save()
      context_extra = {
          'response' : 'Criado com sucesso!',
          'error': False,
      }
    else:
      context_extra = {
          'response' : 'Erros ocorreram!',
          'error': True
      }
   
  else:
        form = PaymentForm()
        if 'action' in request.GET and request.GET['action'] == 'delete':
          item = request.GET['id_delete']
          payment = Payment.objects.get(description__iexact=item)
          payment.delete()
  context = {
    'form': form,
    'payments': Payment.objects.all()
  }
  html_page = render_to_string('expenses/form/new-payment.html', context)
  response = {
    'title' : title,
    'html' : html_page,
    'response' : context_extra['response'] if 'response' in context_extra else None,
    'error': context_extra['error'] if 'error' in context_extra else None,
  }
  return JsonResponse(response, status = 200)

def edit_expense(request):
  title = 'Alterar Gasto'
  context_extra = {}
  if request.POST.get('action') == 'post':
    expense = Expense.objects.get(id=int(request.POST.get('id')))
    form = ExpenseForm(request.POST,instance=expense)
    
    if form.is_valid():
      model = form.save(commit=False)
      model.save()
      context_extra = {
          'response' : 'Alterado com sucesso!',
          'error': False,
      }
    else:
      context_extra = {
          'response' : 'Erros ocorreram!',
          'error': True
      }
   
  else:
    expense = Expense.objects.get(id=request.GET['id'])
    form = ExpenseForm(instance=expense)
  context = {
    'form': form,
    'id_expense': expense.id
  }
  html_page = render_to_string('expenses/form/edit-expense.html', context)
  response = {
    'title' : title,
    'html' : html_page,
    'response' : context_extra['response'] if 'response' in context_extra else None,
    'error': context_extra['error'] if 'error' in context_extra else None,
  }
  return JsonResponse(response, status = 200)


def delete_expense(request,id):
  expense = Expense.objects.get(id=id)
  expense.delete()
  return redirect(reverse('expenses:home'))


################## Relatórios

def list_expenses_by_category(request):
  if request.method == 'POST':
    form = SelectCategoryForm(request.POST)
    if form.is_valid():
      category = form.cleaned_data['category']
      list = Expense.list_expenses_by_category(category)
      context = {
        'form': form,
        'category_selected': category,
        'list':list,
        'page_selected': "report",
      }
      return render(request,'expenses/report/list-expenses-by-category.html',context)
  form = SelectCategoryForm()
  context = {
    'form': form,
    'page_selected': "report",
  }
  return render(request,'expenses/report/list-expenses-by-category.html',context)

def list_expenses_by_category_top(request):
  if request.method == 'POST':
    form = SelectCategoryForm(request.POST)
    if form.is_valid():
      category = form.cleaned_data['category']
      top_category = Expense.list_expenses_by_category_top(category)
      context = {
        'form': form,
        'category_selected': category,
        'top_category':top_category,
        'page_selected': "report",
      }
      return render(request,'expenses/report/list-expenses-by-category-top.html',context)
  form = SelectCategoryForm()
  context = {
    'form': form,
    'page_selected': "report",
  }
  return render(request,'expenses/report/list-expenses-by-category-top.html',context)


from expenses.forms import SelectIntervalPaymentForm
def sum_expenses_payment_and_period(request):
  if request.method == 'POST':
    form = SelectIntervalPaymentForm(request.POST)
    if form.is_valid():
      payment = form.cleaned_data['payment']
      begin = form.cleaned_data['initial']
      end = form.cleaned_data['final']
      total = Expense.sum_expenses_payment_and_period(payment, begin, end)
      context = {
        'form': form,
        'begin' : form.cleaned_data['initial'],
        'end' : form.cleaned_data['final'],
        'payment_selected': payment,
        'total':total,
        'page_selected': "report",
      }
      return render(request,'expenses/report/list-expenses-by-payment-and-period.html',context)
  form = SelectIntervalPaymentForm()
  context = {
    'form': form,
    'page_selected': "report",
  }
  return render(request,'expenses/report/list-expenses-by-payment-and-period.html',context)


from expenses.forms import SelectIntervalExpenseForm
def list_expenses_by_period(request):
  if request.method == 'POST':
    form = SelectIntervalExpenseForm(request.POST)
    if form.is_valid():
      begin = form.cleaned_data['initial']
      end = form.cleaned_data['final']
      list = Expense.list_expenses_by_period(begin, end)
      context = {
        'form': form,
        'begin' : form.cleaned_data['initial'],
        'end' : form.cleaned_data['final'],
        'list_item_expenses': list,
        'page_selected': "report",
      }
      return render(request,'expenses/report/list-expenses-by-period.html',context)
  form = SelectIntervalExpenseForm()
  context = {
    'form': form,
    'page_selected': "report",
  }
  return render(request,'expenses/report/list-expenses-by-period.html',context)


def list_category_by_period(request):
  if request.method == 'POST':
    form = SelectIntervalExpenseForm(request.POST)
    if form.is_valid():
      begin = form.cleaned_data['initial']
      end = form.cleaned_data['final']
      list = Expense.list_category_by_period(begin, end)
      context = {
        'form': form,
        'begin' : form.cleaned_data['initial'],
        'end' : form.cleaned_data['final'],
        'list_categories': list,
        'page_selected': "report",
      }
      return render(request,'expenses/report/list-expenses-by-category-and-period.html',context)
  form = SelectIntervalExpenseForm()
  context = {
    'form': form,
    'page_selected': "report",
  }
  return render(request,'expenses/report/list-expenses-by-category-and-period.html',context)


def list_total_expenses_and_limit(request):
  today = datetime.now()
  expense_first = Expense.objects.all().order_by('date').first()
  date_begin = expense_first.date if expense_first else today
  list_month_year_select = build_list_month_year(date_begin,today)
  list_data = []
  for item_month_year in list_month_year_select:
    month = item_month_year['month_number']
    year = item_month_year['year']
    limit_value = Limit.get_limit_by_month_and_year(month,year)
    expense_value = Expense.get_total_by_month_and_year(month,year)
    list_data.append({
      'month' : get_month_by_number(month),
      'year' : year,
      'limit':limit_value,
      'expense':expense_value,
      'up': expense_value>limit_value
      
    })
    context = {
      'list': list_data,
    }
  
  return render(request,'expenses/report/list_total_expenses_and_limit.html',context)
