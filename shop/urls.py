from django.urls import path
from . import views

urlpatterns = [
    # ... other URL patterns ...
    path('', views.index, name='index'),
    path('purchase/<int:product_id>/', views.PurchaseCreate.as_view(), name='purchase_create'),
]

