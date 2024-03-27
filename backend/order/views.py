from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ItemsSerializer
from item.models import Item


class CartView(APIView):
    """Отображение корзины."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart = request.session.get('cart')

        if cart:

            item_ids = [int(item_id) for item_id in cart.keys() if item_id]
            items_in_cart = Item.objects.filter(
                id__in=item_ids).prefetch_related('tags')

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
        return Response({'message': 'Корзина пуста'},
                        status.HTTP_204_NO_CONTENT)


class AddToCartView(APIView):
    """Добавление товаров в корзину."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity', 1)
        item = get_object_or_404(Item, id=item_id)

        cart = request.session.get('cart', {})
        cart[item_id] = cart.get(item_id, 0) + quantity
        request.session['cart'] = cart

        return Response({
            'message': 'Товар добавлен в корзину',
            'item': {
                'id': item.id,
                'name': item.name,
                'quantity': quantity,
                'price': item.price,
                'total_price': item.price * quantity if item.price else item.discount_price * quantity
            }
        },
            status=status.HTTP_201_CREATED)


class DeleteCartView(APIView):
    """Удаление корзины."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        try:
            del request.session['cart']
            return Response({'message': 'Содержимое корзины очищено'},
                            status.HTTP_200_OK)
        except KeyError:
            return Response({'message': 'Корзина пуста'},
                            status.HTTP_204_NO_CONTENT)
