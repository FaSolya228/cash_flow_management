
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from rest_framework import viewsets

from apps.cash_flow.filters import CashFlowFilterSet
from apps.cash_flow.forms import CashFlowForm
from apps.cash_flow.models import CashFlow, CashFlowCategory
from apps.cash_flow.serializers import CashFlowCategorySerializer


# Create your views here.
class CashFlowCategoryViewSet(viewsets.ModelViewSet):
    queryset = CashFlowCategory.objects.select_related(
        'parent',
        'type',
    ).all()
    serializer_class = CashFlowCategorySerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'type': ['exact'],
        'parent': ['exact', 'isnull'],
    }

class CashFlowListView(FilterView):
    queryset = CashFlow.objects.select_related(
        'category',
        'category__parent',
        'type',
        'status',
    ).all().order_by('-creation_date')
    template_name = 'cash_flow/list.html'
    filterset_class = CashFlowFilterSet

class CashFlowCreateView(CreateView):
    model = CashFlow
    template_name = 'cash_flow/create.html'
    success_url = '/cash_flows'
    form_class = CashFlowForm

class CashFlowUpdateView(UpdateView):
    model = CashFlow
    template_name = 'cash_flow/create.html'
    success_url = '/cash_flows'
    form_class = CashFlowForm

class CashFlowDeleteView(DeleteView):
    model = CashFlow
    template_name = 'cash_flow/list.html'
    success_url = '/cash_flows'