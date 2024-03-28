from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (ItemsSerializer, UpdateCartSerializer,
                             AddToCartSerializer)
from item.models import Item


class CartCheck:
    """Класс проверок для корзины."""

    @staticmethod
    def clear_cart_from_zeroes_quantities(request):
        """Очистка корзины от товаров с нулевым значением количества."""

        cart = request.session['cart']
        non_zero_quantity_items = {item_id: quantity for item_id, quantity
                                   in cart.items() if quantity > 0}

        if len(non_zero_quantity_items) < len(cart):
            request.session['cart'] = non_zero_quantity_items
            request.session.modified = True

        return non_zero_quantity_items


class CartView(APIView):
    """Отображение корзины."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart = request.session.get('cart')

        if not cart or all(quantity == 0 for quantity in cart.values()):
            return Response({'message': 'Корзина пуста'},
                            status.HTTP_204_NO_CONTENT)

        item_ids = [int(item_id) for item_id in cart.keys()]

        non_zero_quantity_items = {item_id: quantity for item_id, quantity in cart.items() if quantity > 0}

        if len(non_zero_quantity_items) < len(cart):
            request.session['cart'] = non_zero_quantity_items
            request.session.modified = True

        items_in_cart = Item.objects.filter(
            id__in=non_zero_quantity_items).prefetch_related('tags')

        # Т.к. в request.session ключи всегда строки,
        # даже если исходные ключи были числами, то передаем str(item_id).
        total_quantity = sum(cart[str(item_id)] for item_id in item_ids)

        quantity_per_item = [quantity for quantity in cart.values()]

        price_per_item = [item.discount_price if item.is_discount else
                          item.price for item in items_in_cart]

        cart_total_price = sum([price_per_item * quantity_per_item for
                                price_per_item, quantity_per_item in
                                zip(price_per_item, quantity_per_item)])

        serializer = ItemsSerializer(items_in_cart, many=True)

        for item_data, quantity, price_per_item in zip(serializer.data,
                                                       quantity_per_item,
                                                       price_per_item):
            item_data['quantity'] = quantity
            item_data['price_for_all_items'] = quantity * price_per_item

        return Response({'total_quantity': total_quantity,
                         'cart_total_price': cart_total_price,
                         'items': serializer.data})


class AddToCartView(APIView):
    """Добавление товаров в корзину."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item_id = serializer.validated_data['item_id']
        quantity = serializer.validated_data.get('quantity', 1)

        item = get_object_or_404(Item, id=item_id)
        cart = request.session.get('cart', {})

        if str(item.id) in cart.keys() and cart[str(item_id)] > 0:
            return Response({'message': 'Вы уже добавили этот товар в корзину'}, status.HTTP_302_FOUND)

        cart[item_id] = cart.get(item_id, 0) + quantity
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

        serializer = UpdateCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            CartCheck.clear_cart_from_zeroes_quantities(request)

            # Не использую get('cart', {}) намеренно, чтобы при ошибке
            # не создавать пустую козину, а лишь проверить на существование
            cart = request.session['cart']

            item_id = serializer.validated_data['item_id']
            item_quantity = serializer.validated_data['quantity']

            if str(item_id) in cart.keys():
                if cart[str(item_id)] <= 0:
                    return Response({'error': 'Количество товаров не может быть отрицательным'}, status.HTTP_400_BAD_REQUEST)
                if int(-item_quantity) > cart[str(item_id)]:
                    return Response({'error': 'В корзине нет такого количества товара'}, status.HTTP_400_BAD_REQUEST)
                cart[str(item_id)] += int(item_quantity)
                request.session['cart'] = cart
                return Response({'message': 'Количество товара обновлено'}, status.HTTP_201_CREATED)
            return Response({'error': 'Такого товара нет в корзине'}, status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'error': 'Нельзя обновить количество товаров в пустой корзине'}, status.HTTP_400_BAD_REQUEST)


class DeleteCartView(APIView):
    """Удаление содержимого корзины."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """POST-запрос для очистки корзины от содержимого."""

        if 'cart' in request.session:
            # del request.session['cart']
            request.session['cart'] = {}
            return Response({'message': 'Содержимое корзины очищено'},
                            status.HTTP_200_OK)

        return Response({'message': 'Корзина пуста'},
                        status.HTTP_204_NO_CONTENT)
