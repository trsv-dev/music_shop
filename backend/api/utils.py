import socket
from smtplib import SMTPException
from celery import shared_task
from django.apps import apps

from django.conf import settings
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import render_to_string

from music_shop.settings import TEMPLATES_DIR

templates = {
    'to_admin_about_new_order':
        f'{TEMPLATES_DIR}/email_templates/to_admin_about_new_order.html',
    'to_customer_about_new_order':
        f'{TEMPLATES_DIR}/email_templates/to_customer_about_new_order.html',
    'to_customer_about_status_changes':
        f'{TEMPLATES_DIR}/email_templates/to_customer_about_status_changes.html',
}


def get_total_price(order_items):
    """Вычисление общей суммы заказа."""

    return sum(
        (order_item.item.discount_price if order_item.item.is_discount else
         order_item.item.price) * order_item.quantity for
        order_item in order_items
    )


def get_template_and_email(order, recipient_type):
    """Определение шаблона письма и адресата."""

    if recipient_type == 'admin':
        template_name = templates['to_admin_about_new_order']
        recipient_email = settings.ADMIN_EMAIL
    elif recipient_type == 'customer':
        template_name = templates['to_customer_about_new_order']
        recipient_email = order.email
    else:
        template_name = templates['to_customer_about_status_changes']
        recipient_email = order.email

    return template_name, recipient_email


@shared_task
def send_email_message(order_id, order_item_ids=None, recipient_type=None):
    """
    Отправка писем на электронную почту.
    """

    # Получаем модели так для избежания циклического импорта.
    Order = apps.get_model('order', 'Order')
    OrderItem = apps.get_model('order', 'OrderItem')

    if not order_item_ids:
        order_item_ids = []

    if recipient_type not in ['admin', 'customer', 'status_changed']:
        raise ValueError(
            "Недопустимое значение recipient_type. "
            "Допустимые значения: 'admin', 'customer, 'status_changed'")

    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(id__in=order_item_ids)

    total_price = get_total_price(order_items)
    total_price_formatted = f'{total_price:,} руб.'

    context = {
        'first_name': order.first_name,
        'last_name': order.last_name,
        'order_items': order_items,
        'order_number': order.order_number,
        'order_status': order.status,
        'order_date': order.created_date,
        'total_price': total_price_formatted,
        'customer_email': order.email,
        'communication_method': order.communication_method
    }

    template, email = get_template_and_email(order, recipient_type)
    message = render_to_string(template_name=template, context=context)

    try:
        send_mail(
            subject='Письмо от Music Shop',
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=message
        )
    except socket.gaierror as e:
        print(f'Временный сбой в разрешении имени: {e}')
        raise
    except SMTPException as e:
        print(f'Ошибка SMTP: {e}')
        raise
