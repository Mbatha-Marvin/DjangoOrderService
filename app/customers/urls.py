from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView

urlpatterns = [
    path("", CustomerListCreateView.as_view(), name="customer-list-create"),
    path("<uuid:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
]
