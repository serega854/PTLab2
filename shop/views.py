from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import Product, Purchase

def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)

class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['person', 'address']  # Убираем product из полей формы, чтобы не было путаницы

    def get_initial(self):
        initial = super().get_initial()
        initial['product'] = Product.objects.get(pk=self.kwargs['product_id'])
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        product = Product.objects.get(pk=self.kwargs['product_id'])
        initial_quantity = product.quantity

        if initial_quantity > 0:
            product.quantity -= 1
            
            # Увеличиваем цену на 20%, если количество уменьшилось более чем в два раза
            if product.quantity < (initial_quantity / 2):
                product.price *= 1.2
            
            product.save()
            self.object.product = product  # Присваиваем продукт к покупке
            self.object.save()

            return HttpResponse(f'Спасибо за покупку, {self.object.person}!')
        else:
            return HttpResponse('Извините, товар закончился.')
