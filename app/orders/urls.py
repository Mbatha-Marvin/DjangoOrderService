from django.urls import path
from .views import OrderListCreateView, OrderDetailView

urlpatterns = [
    path("", OrderListCreateView.as_view(), name="order-list-create"),
    path("<uuid:pk>/", OrderDetailView.as_view(), name="order-detail"),
]
