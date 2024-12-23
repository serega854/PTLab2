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
            return HttpResponse('Извините, товар закончился.', status=400)

        person = request.POST.get('person')
        address = request.POST.get('address')

        if not person or not address:
            return HttpResponse('Пожалуйста, заполните все поля.', status=400)  # Проверка на заполнение полей

        # Обновление количества товара
        product.quantity -= 1

        # Проверка на снижение цены
        if product.quantity <= product.quantity_beg / 2:  
            product.price *= Decimal(1.2)  

        product.save()  # Сохранение обновленного товара

        # Создание новой записи о покупке
        try:
            ShopPurchase.objects.create(person=person, address=address, product=product)
        except Exception as e:
            return HttpResponse(f'Ошибка при создании записи: {str(e)}', status=500)

        # Возвращаем статус 200 при успешной покупке
        return HttpResponse(f'Спасибо за покупку, {person}!', status=200)  # Здесь добавлен статус 200
