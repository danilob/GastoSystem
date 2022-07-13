from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Category(models.Model):
    description = models.CharField("Categoria", max_length=150,primary_key=True)
    create_date = models.DateField("Data de Criação",auto_now=True)

    class Meta:
      ordering = ["description"]
      verbose_name = "Categoria de Gasto"
      verbose_name_plural = "Categoria de Gastos"

    def __str__(self):
      return f'{self.description.upper()}'

    def is_possible_delete(self):
      return not self.related_category.exists()

class Payment(models.Model):
    description = models.CharField("Forma de Pagamento", max_length=150,primary_key=True)
    create_date = models.DateField("Data de Criação",auto_now=True)
    
    class Meta:
      ordering = ["description"]
      verbose_name = "Categoria de Pagamento"
      verbose_name_plural = "Categoria de Pagamentos"

    def __str__(self):
      return f'{self.description.upper()}'

    def is_possible_delete(self):
      return not self.related_payment.exists()


class Expense(models.Model):
    category = models.ForeignKey(Category,
            on_delete=models.RESTRICT,
            related_name='related_category'
            )
    payment = models.ForeignKey(Payment,
            on_delete=models.RESTRICT,
            related_name='related_payment'
            )
    date = models.DateField("Data")
    value = models.DecimalField("Valor",max_digits=6,decimal_places=2)
    description = models.CharField("Descrição", max_length=150)

    class Meta:
      ordering = ["-date","-value","category"]
      verbose_name = "Gasto"
      verbose_name_plural = "Gastos"
      constraints = [
            models.UniqueConstraint(
                fields=('category', 'payment','date','description'), name='unique_expense'
            )
        ]

    def __str__(self):
      return f'{self.category.description.upper()} -{self.description.upper()} ({self.value})'

    @staticmethod
    def list_expenses_by_category(category):
      from django.db.models import Sum
      return Expense.objects.filter(category=category).values(
        'date__year','date__month'
        ).annotate(total=Sum('value')).order_by(
          '-date__year','-date__month'
          )

    def clean(self):
      if self.value<0:
        raise ValidationError(f'''O valor '{self.value}' é inválido
            - o valor deve ser maior ou igual a zero.''')
      super(Expense, self).clean()

    def save(self, *args, **kwargs):
      self.full_clean()
      super(Expense, self).save(*args, **kwargs)

class Limit(models.Model):
    year = models.IntegerField("Ano")
    month = models.IntegerField("Mês")
    value = models.DecimalField("Valor",max_digits=6,decimal_places=2)

    class Meta:
      ordering = ["-year","-month"]
      verbose_name = "Limite Mensal"
      verbose_name_plural = "Limites Mensais"
      constraints = [
            models.UniqueConstraint(
                fields=('month', 'year'), name='unique_expense_limit_by_month_year'
            )
        ]

    def __str__(self):
      return f'{self.month}/{self.year} - {self.value}'

    def clean(self):
      if self.month>12 or self.month<1:
        raise ValidationError(f'''O mês '{self.month}' é inválido
          - o mês deve ser um número entre [1,12].''')
      if self.value<0:
        raise ValidationError(f'''O valor '{self.value}' é inválido
            - o valor deve ser maior ou igual a zero.''')
      super(Limit, self).clean()

    def save(self, *args, **kwargs):
      self.full_clean()
      super(Limit, self).save(*args, **kwargs)