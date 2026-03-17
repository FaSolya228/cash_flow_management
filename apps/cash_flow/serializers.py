from rest_framework import serializers

from apps.cash_flow.models import CashFlowCategory


class CashFlowCategorySerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.name', read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True, default=None)

    class Meta:
        model = CashFlowCategory
        fields = (
            'id',
            'name',
            'parent_name',
            'type_name',
        )