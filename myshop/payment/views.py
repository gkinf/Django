# print("Debugging: Stopping execution here.")
# breakpoint() 
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order
from paypal.standard.forms import PayPalPaymentsForm

def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        # PayPal transaction data
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': str(order.get_total_cost()),  # Total order cost
            'item_name': f'Order {order.id}',  # Order description
            'invoice': str(order.id),  # Unique order ID
            'currency_code': 'USD',  # Currency for the payment
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),  # IPN URL
            'return_url': success_url,  # Successful payment redirect
            'cancel_return': cancel_url,  # Cancelled payment redirect
        }

        # Add individual order items to PayPal dictionary (optional)
        item_count = 1
        for item in order.items.all():
            paypal_dict[f'item_name_{item_count}'] = item.product.name
            paypal_dict[f'amount_{item_count}'] = str(item.price)
            paypal_dict[f'quantity_{item_count}'] = item.quantity
            item_count += 1

        # Create PayPal form
        form = PayPalPaymentsForm(initial=paypal_dict)

        # Redirect to PayPal
        return render(request, 'payment/process.html', {'order': order, 'form': form})
    
    return render(request, 'payment/process.html', {'order': order})



def payment_completed(request):
    return render(request, 'payment/completed.html')
def payment_canceled(request):
    return render(request, 'payment/canceled.html')

