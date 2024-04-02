import socket
from smtplib import SMTPException

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
}


def send_email_message(order, order_item, recipient_type=None):
    """
    Отправка писем на электронную почту.
    """

    if recipient_type not in ['admin', 'customer']:
        raise ValueError(
            "Недопустимое значение recipient_type. "
            "Допустимые значения: 'admin', 'customer.")

    total_price = sum(
        (order_item.item.discount_price if order_item.item.is_discount else
         order_item.item.price) * order_item.quantity for
        order_item in order_item)

    total_price_formatted = f'{total_price:,} руб.'

    context = {
        'first_name': order.first_name,
        'last_name': order.last_name,
        'order_item': order_item,
        'order_number': order.order_number,
        'order_date': order.created_date,
        'total_price': total_price_formatted,
        'customer_email': order.email,
        'communication_method': order.communication_method
    }

    if recipient_type == 'admin':
        template_name = templates['to_admin_about_new_order']
        recipient_email = settings.ADMIN_EMAIL
    else:
        template_name = templates['to_customer_about_new_order']
        recipient_email = order.email

    message = render_to_string(template_name=template_name, context=context)

    try:
        send_mail(
            subject='Письмо от Music Shop',
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[recipient_email],
            html_message=message
        )
    except socket.gaierror as e:
        print(f'Временный сбой в разрешении имени: {e}')
        raise
    except SMTPException as e:
        print(f'Ошибка SMTP: {e}')
        raise
