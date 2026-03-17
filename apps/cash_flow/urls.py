from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.cash_flow.views import CashFlowCategoryViewSet, CashFlowListView, CashFlowCreateView, CashFlowUpdateView, \
    CashFlowDeleteView

router = DefaultRouter()
router.register(r'categories', CashFlowCategoryViewSet, basename='cashflow_category')

urlpatterns = [
    path('cash_flows/', CashFlowListView.as_view(), name='cashflow_list'),
    path('cash_flows/create/', CashFlowCreateView.as_view(), name='cashflow_create'),
    path('cash_flows/<int:pk>/edit/', CashFlowUpdateView.as_view(), name='cashflow_edit'),
    path('cash_flows/<int:pk>/delete/', CashFlowDeleteView.as_view(), name='cashflow_delete'),

    path('api/v1/', include(router.urls))
]