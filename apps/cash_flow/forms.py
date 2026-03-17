from datetime import date

from django.forms import ModelForm, Select, TextInput, NumberInput, ModelChoiceField, DateInput, DateField

from apps.cash_flow.models import CashFlow, CashFlowCategory
from apps.cash_flow.utils import CategoryDependentMixin


class CashFlowForm(CategoryDependentMixin, ModelForm):
    category = ModelChoiceField(
        queryset=CashFlowCategory.objects.filter(parent__isnull=True),
        label="Категория",
        required=True,
        widget=Select(attrs={'id': 'id_category', 'class': 'form-select'})
    )
    subcategory = ModelChoiceField(
        queryset=CashFlowCategory.objects.filter(parent__isnull=False),
        required=True,
        label="Подкатегория",
        widget=Select(attrs={'id': 'id_subcategory', 'class': 'form-select'})
    )
    creation_date = DateField(
        initial=date.today,
        label="Дата создания",
        widget=DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            },
            format='%Y-%m-%d'
        )
    )

    class Meta:
        model = CashFlow
        fields = [
            'type',
            'subcategory',
            'amount',
            'status',
            'comment',
            'creation_date'
        ]
        widgets = {
            "type": Select(attrs={
                'class': 'form-select'
            }),
            "amount": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Сумма в рублях...",
                'min': '0.01',
                'required': 'required'
            }),
            "status": Select(attrs={
                'class': 'form-select'
            }),
            "comment": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Комментарий..."
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # При редактировании вычисляем родительскую категорию для отображения
        if self.instance.pk and self.instance.category.parent:
            self.initial['subcategory'] = self.instance.category
            self.initial['category'] = self.instance.category.parent

            self.fields['subcategory'].widget.attrs['data-selected'] = self.instance.category_id # Чтобы форма видела подкатегорию

        # Синхронизируем связанные поля (тип, категория и подкатегория) для их отображения
        self.sync_category_queries(self.data, self.instance)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')

        if amount and amount <= 0:
            self.add_error('amount', "Сумма должна быть > 0!")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        subcategory = self.cleaned_data.get('subcategory')
        category = self.cleaned_data.get('category')

        # Если выбрана подкатегория — сохраняем её, иначе — главную категорию
        if subcategory:
            instance.category = subcategory
        else:
            instance.category = category

        if commit:
            instance.save()
        return instance