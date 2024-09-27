from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.core.exceptions import ObjectDoesNotExist

@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    try:
        # Fetch the order using the given order_id
        order = Order.objects.get(id=order_id)

        # Email subject and message
        subject = f'Order nr. {order.id}'
        message = f'Dear {order.first_name},\n\n' \
                  f'You have successfully placed an order.' \
                  f'Your order ID is {order.id}.'

        # Send the email
        mail_sent = send_mail(subject,
                              message,
                              'business@centennialinfotech.com',
                              [order.email])
        return mail_sent

    except ObjectDoesNotExist:
        # Handle the case where the order doesn't exist
        print(f"Order with ID {order_id} does not exist.")
        return False
