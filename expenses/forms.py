from django import forms
from django.core.exceptions import ValidationError
from expenses.admin import PaymentAdmin
from expenses.models import Category

class SelectCategoryForm(forms.Form):
    category = forms.ModelChoiceField(label="Categoria",queryset=Category.objects.all())

from expenses.models import Expense

from django.core.exceptions import ValidationError

from expenses.models import Category

from expenses.models import Payment

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['description']
        
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['description']
    
class EditExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category','payment','description','value','date']
        labels = {
            'category': 'Categoria',
            'payment': 'Pagamento'
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category','payment','description','value','date']
        labels = {
            'category': 'Categoria',
            'payment': 'Pagamento'
        }
        #exclude = ['',...]

    # def clean_coach(self):
    #     data = self.cleaned_data['coach']
    #     if not (data):
    #         raise ValidationError("É obrigatório adicionar o treinador.")

    #     return data