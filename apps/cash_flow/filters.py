
import django_filters
from django.forms import DateTimeInput, Select, DateInput

from apps.cash_flow.models import CashFlow, CashFlowCategory, CashFlowType, CashFlowStatus
from apps.cash_flow.utils import CategoryDependentMixin


class CashFlowFilterSet(django_filters.FilterSet):
    date_start = django_filters.DateFilter(
        field_name='creation_date',
        lookup_expr='gte',
        label='Начало периода',
        widget=DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            },
            format='%d-%m-%Y'
        )
    )
    date_end = django_filters.DateFilter(
        field_name='creation_date',
        lookup_expr='lte',
        label='Конец периода',
        widget=DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            },
            format='%d-%m-%Y'
        )
    )
    type = django_filters.ModelChoiceFilter(
        queryset=CashFlowType.objects.filter(),
        label="Тип"
    )
    status = django_filters.ModelChoiceFilter(
        queryset=CashFlowStatus.objects.filter(),
        label="Статус"
    )
    category = django_filters.ModelChoiceFilter(
        queryset=CashFlowCategory.objects.filter(parent__isnull=True),
        field_name="category__parent",
        label="Категория",
        widget = Select({'id': 'id_category'})
    )
    subcategory = django_filters.ModelChoiceFilter(
        queryset=CashFlowCategory.objects.filter(parent__isnull=False),
        field_name="category",
        label="Подкатегория",
        widget=Select({'id': 'id_subcategory'})
    )

    class Meta:
        model = CashFlow
        fields = ('date_start', 'date_end', 'type', 'status', 'category', 'subcategory')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        CategoryDependentMixin.sync_category_queries(self.form, self.data)

        # Стилизация полей для фильтрации
        for name, field in self.form.fields.items():
            if isinstance(field.widget, Select):
                field.widget.attrs.update({'class': 'form-select form-select-sm'})
            else:
                field.widget.attrs.update({'class': 'form-control form-control-sm'})