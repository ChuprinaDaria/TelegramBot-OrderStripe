import stripe
import os
import logging
from datetime import datetime, timedelta

stripe.api_key = os.getenv("STRIPE_API_KEY")

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_payment_link(amount, description):
    success_url = os.getenv("SUCCESS_URL")
    cancel_url = os.getenv("CANCEL_URL")
    
    if not success_url or not cancel_url:
        raise ValueError("SUCCESS_URL і CANCEL_URL повинні бути встановлені")

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': description,
                },
                'unit_amount': int(amount * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    logger.info(f"Посилання на оплату створено: {session.url}")
    return session.url

def remind_payment(user_id, order_id, amount, description):
    payment_link = create_payment_link(amount, description)
    logger.info(f"Нагадування про оплату відправлено користувачу {user_id} для замовлення {order_id}")
    # Логіка для надсилання повідомлення з нагадуванням користувачеві з посиланням на оплату
    # Це можна інтегрувати з бібліотекою планування, наприклад APScheduler, для планування нагадувань