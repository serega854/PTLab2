from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import Product, Purchase


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['person', 'address']
    
    def get_initial(self):
        initial = super().get_initial()
        try:
            product = get_object_or_404(Product, pk=self.kwargs['product_id'])
            initial['product'] = product
        except Exception as e:
            print(e)  # Логирование ошибки
        
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])

        # Получаем начальное количество из базы данных
        initial_quantity = product.quantity
        
        if product.quantity > 0:
            previous_quantity = product.quantity
            product.quantity -= 1

            # Проверяем, уменьшилось ли количество более чем в два раза
            if previous_quantity > 0 and product.quantity <= (initial_quantity // 2):  # Условие деления пополам
                product.price *= 0.8  # Уменьшаем цену на 20%
                print(f"Цена товара {product.name} изменена на {product.price}")

            product.save()  # Сохранение изменений количества и цены
            self.object.product = product
            self.object.save()
            
            return HttpResponse(f'Спасибо за покупку, {self.object.person}!')
        else:
            return HttpResponse('Извините, товар закончился.')