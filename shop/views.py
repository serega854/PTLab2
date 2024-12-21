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
        # Use get_object_or_404 for better error handling
        initial['product'] = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        product = self.object.product # Get product from the form directly

        initial_quantity = product.quantity

        if initial_quantity > 0:
            product.quantity -= 1
            product.save()  # Save the product before checking the quantity

            if product.quantity * 2 < initial_quantity:
                product.price *= 1.2
                product.save() #Save after price update

            self.object.save()
            return HttpResponse(f'Спасибо за покупку, {self.object.person}!')
        else:
            return HttpResponse('Извините, товар закончился.')

