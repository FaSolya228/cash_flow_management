from apps.cash_flow.models import CashFlowCategory

# Миксина для синхронизации queryset'ов при выборе данных в связанных полях "Тип", "Категория", "Подкатегория"
class CategoryDependentMixin:
    def sync_category_queries(self, data, instance=None):
        type_id = data.get('type') or getattr(instance, 'type_id', None)
        category_id = data.get('category') or getattr(instance, 'category_id', None)

        if not category_id and instance and hasattr(instance, 'category') and instance.category:
            if instance.category.parent_id:
                category_id = instance.category.parent_id
            else:
                category_id = instance.category_id

        # Родительские категории
        if 'category' in self.fields:
            qs = CashFlowCategory.objects.filter(parent__isnull=True)
            if type_id:
                qs = qs.filter(type_id=type_id)
            self.fields['category'].queryset = qs.distinct()

        # Подкатегории
        if 'subcategory' in self.fields:
            sub_qs = CashFlowCategory.objects.filter(parent__isnull=False)
            if category_id:
                sub_qs = sub_qs.filter(parent_id=category_id)
            elif type_id:
                sub_qs = sub_qs.filter(type_id=type_id)

            # Оставляем все подкатегории, чтобы поле не было пустым
            self.fields['subcategory'].queryset = sub_qs.distinct()
