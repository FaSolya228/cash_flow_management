from django.contrib import admin

from apps.cash_flow.models import CashFlowType, CashFlowCategory, CashFlowStatus


# Register your models here.
@admin.register(CashFlowType)
class CashFlowTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(CashFlowCategory)
class CashFlowCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'type')
    search_fields = ('name', 'parent', 'type')
    list_filter = ('parent', 'type')

@admin.register(CashFlowStatus)
class CashFlowStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
