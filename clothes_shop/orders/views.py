from django.shortcuts import render
from django.views import View

from .forms import OrderCreateForm
from .models import OrderItem

from cart.cart import Cart


class OrderView(View):
    """
    Описывает зстраницу оформления заказа и просмотра данных о уже выполненном
    заказе

    1. post -> создание нового заказа
    2. get -> просмотр информации о уже созданном заказе
    """
    @staticmethod
    def post(request):
        """
        Обработка формы создания нового заказа
        - проверка валидности данных
        - создание заказа
        - очистка корзины
        - показ страницы успешной регистрации заказа
          TODO: оплата (?)
        """
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        # TODO: if not form.is_valid()
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order})

    @staticmethod
    def get(request):
        """
        Отображение формы регистрации заказа
        """
        cart = Cart(request)
        form = OrderCreateForm
        return render(request, 'orders/order/create.html',
                      {'cart': cart, 'form': form})