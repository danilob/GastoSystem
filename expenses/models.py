from django.db import models

class Category(models.Model):
    description = models.CharField("Categoria", max_length=150,primary_key=True)

    class Meta:
      ordering = ["description"]
      verbose_name = "Categoria de Gasto"
      verbose_name_plural = "Categoria de Gastos"

    def __str__(self):
      return f'{self.description.upper()}'

class Payment(models.Model):
    description = models.CharField("Forma de Pagamento", max_length=150,primary_key=True)

    class Meta:
      ordering = ["description"]
      verbose_name = "Categoria de Pagamento"
      verbose_name_plural = "Categoria de Pagamentos"

    def __str__(self):
      return f'{self.description.upper()}'


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