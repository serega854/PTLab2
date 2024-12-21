# shop/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from decimal import Decimal
from .models import Product, ShopPurchase

def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)

class PurchaseCreate(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, 'shop/purchase_form.html', {'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)

        if product.quantity <= 0:
            return HttpResponse('Извините, товар закончился.')

        person = request.POST['person']
        address = request.POST['address']

        # Update product quantity
        product.quantity -= 1

        # Check if quantity is less than or equal to half of original
        if product.quantity <= product.quantity_beg / 2:  # Use integer division
            product.price *= Decimal(1.2)  # Convert 1.2 to Decimal
        
        product.save()  # Save updated product

        # Create a new Purchase entry
        ShopPurchase.objects.create(person=person, address=address, product=product)

        return HttpResponse(f'Спасибо за покупку, {person}!')
