from django import forms
from django.core.exceptions import ValidationError

from expenses.models import Category

class SelectCategoryForm(forms.Form):
    category = forms.ModelChoiceField(label="Categoria",queryset=Category.objects.all())