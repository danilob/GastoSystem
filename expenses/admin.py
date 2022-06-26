from django.contrib import admin

from expenses.models import Category

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)

from expenses.models import Payment

class PaymentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Payment, PaymentAdmin)


from expenses.models import Expense

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description','category','value','date')

admin.site.register(Expense, ExpenseAdmin)


from expenses.models import Limit

class LimitAdmin(admin.ModelAdmin):
    pass

admin.site.register(Limit, LimitAdmin)
