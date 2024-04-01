from django.core.exceptions import SuspiciousOperation
from django.db import transaction
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (ItemsSerializer, UpdateCartSerializer,
                             AddToCartSerializer, OrderSerializer)
from item.models import Item
from order.models import Order, OrderItem


class CartChecker:
    """Класс проверок для корзины."""

    def get_cart(self, request):
        """Получение корзины."""

        try:
            cart = request.session['cart']
            return cart
        except KeyError:
            raise SuspiciousOperation('Корзина не найдена')

    def get_cart_items(self, request):
        """Получение товаров, имеющий такой же id, как ключи корзины."""

        cart = self.get_cart(request)

        return Item.objects.filter(
            id__in=cart.keys(), is_published=True
        ).prefetch_related('tags').order_by('id')

    def del_unexisting_items_and_zeros_quantities(self, request):
        """
        Очистка корзины от товаров с нулевым значением количества.
        Очистка от отсутствующих товаров.
        """

        cart = self.get_cart(request)

        # Проверяем, что все товары из корзины всё еще в БД. Сортируем по ID.
        cart_items = self.get_cart_items(request)
        existing_non_zero_quantity_items = {}

        for item in cart_items:
            quantity = cart.get(str(item.id), 0)
            if quantity > 0:
                existing_non_zero_quantity_items[str(item.id)] = quantity

        existing_non_zero_quantity_items = sorted(
            existing_non_zero_quantity_items.items(), key=lambda x: x[0]
        )
        sorted_existing_non_zero_quantity_items = {
            key: value for key, value in existing_non_zero_quantity_items
        }

        if len(sorted_existing_non_zero_quantity_items) < len(cart):
            request.session['cart'] = sorted_existing_non_zero_quantity_items
            request.session.modified = True

        return sorted_existing_non_zero_quantity_items


class CartView(APIView):
    """Отображение корзины."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """GET-запрос для просмотра товаров в корзине."""

        cart_checker = CartChecker()
        cart = cart_checker.del_unexisting_items_and_zeros_quantities(request)

        if not cart or all(quantity == 0 for quantity in cart.values()):
            return Response({'message': 'Корзина пуста'},
                            status.HTTP_204_NO_CONTENT)

        item_ids = sorted([int(item_id) for item_id in cart.keys()])

        items_in_cart = Item.objects.filter(
            id__in=cart).prefetch_related('tags').order_by('id')

        # Т.к. в request.session ключи всегда строки,
        # даже если исходные ключи были числами, то передаем str(item_id).
        total_quantity = sum(cart[str(item_id)] for item_id in item_ids)

        quantity_per_item = len(set(item_key for item_key in cart.keys()))

        all_items_quantity = [quantity for quantity in cart.values()]

        price_per_item = [item.discount_price if item.is_discount else
                          item.price for item in items_in_cart]

        cart_total_price = sum([price_per_item * quantity_per_item for
                                price_per_item, quantity_per_item in
                                zip(price_per_item, all_items_quantity)])

        serializer = ItemsSerializer(items_in_cart, many=True)

        for item_data, quantity, price_per_item in zip(serializer.data,
                                                       all_items_quantity,
                                                       price_per_item):
            item_data['quantity'] = quantity
            item_data['price_for_all_items'] = quantity * price_per_item

        return Response({'total_quantity': total_quantity,
                         'quantity_per_item': quantity_per_item,
                         'cart_total_price': cart_total_price,
                         'items': serializer.data})


class AddToCartView(APIView):
    """Добавление товаров в корзину."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """POST-запрос для добавления товаров в корзину."""

        cart_checker = CartChecker()
        cart = cart_checker.del_unexisting_items_and_zeros_quantities(request)

        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item_id = serializer.validated_data['item_id']
        quantity = serializer.validated_data.get('quantity', 1)

        item = get_object_or_404(Item, id=item_id)

        if str(item.id) in cart.keys() and cart[str(item_id)] > 0:
            return Response(
                {'message': 'Вы уже добавили этот товар в корзину'},
                status.HTTP_302_FOUND)

        cart[str(item_id)] = cart.get(item_id, 0) + quantity
        request.session['cart'] = cart

        return Response({
            'message': 'Товар добавлен в корзину',
            'item': {
                'id': item.id,
                'name': item.name,
                'quantity': quantity,
                'price': item.price,
                'total_price': item.price * quantity if item.price else
                item.discount_price * quantity
            }
        }, status=status.HTTP_201_CREATED)


class UpdateCartView(APIView):
    """Обновление содержания корзины."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """POST-запрос для обновления количества товаров в корзине."""

        cart_checker = CartChecker()

        serializer = UpdateCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Проверяем, что в корзине что-то есть.
            cart = cart_checker.del_unexisting_items_and_zeros_quantities(request)
            item_id = str(serializer.validated_data['item_id'])
            item_quantity = serializer.validated_data['quantity']

            if item_id in cart.keys():
                if cart[item_id] <= 0:
                    return Response({
                        'error': 'Количество товаров не '
                                 'может быть отрицательным'
                    }, status.HTTP_400_BAD_REQUEST)
                if int(-item_quantity) > cart[item_id]:
                    return Response(
                        {'error': 'В корзине нет такого количества товара'},
                        status.HTTP_400_BAD_REQUEST)
                cart[item_id] += int(item_quantity)

                request.session['cart'] = cart
                return Response({'message': 'Количество товара обновлено'},
                                status.HTTP_201_CREATED)
            return Response({'error': 'Такого товара нет в корзине'},
                            status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({
                'error': 'Нельзя обновить количество товаров '
                         'в пустой корзине'
            }, status.HTTP_400_BAD_REQUEST)


class DeleteCartView(APIView):
    """Удаление содержимого корзины."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """POST-запрос для очистки корзины от содержимого."""

        if 'cart' in request.session:
            request.session['cart'] = {}
            return Response({'message': 'Содержимое корзины очищено'},
                            status.HTTP_200_OK)

        return Response({'message': 'Корзина пуста'},
                        status.HTTP_204_NO_CONTENT)


class CheckoutView(APIView):
    """Оформление заказа."""

    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request):
        """POST-запрос для оформления заказа."""

        cart_checker = CartChecker()
        cart = cart_checker.del_unexisting_items_and_zeros_quantities(request)

        # Если корзина пуста или содержит товары с нулевым количеством -
        # показываем ошибку о пустой корзине.
        if not cart:
            return Response({'error': 'Оформлять нечего. Корзина пуста'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Order(
            first_name=serializer.validated_data.get('first_name'),
            last_name=serializer.validated_data.get('last_name'),
            address=serializer.validated_data.get('address'),
            email=serializer.validated_data.get('email'),
            communication_method=serializer.validated_data.get(
                'communication_method'),
            order_notes=serializer.validated_data.get('order_notes')
        )
        order.save()

        cart_items = cart_checker.get_cart_items(request)
        order_item = [OrderItem(order=order, item=item, quantity=quantity) for
                      quantity, item in
                      zip(cart.values(), cart_items)]

        OrderItem.objects.bulk_create(order_item)

        request.session['cart'] = {}
        request.session.modified = True

        return Response({'message': 'Заказ успешно оформлен'},
                        status.HTTP_201_CREATED)
