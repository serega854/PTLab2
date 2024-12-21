from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Added to handle the main page
    path('buy/<int:product_id>/', views.PurchaseCreate.as_view(), name='buy'),
]
