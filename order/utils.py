from django.core.mail import send_mail


def send_confirmation_mail(user, activation_code):
    message = f"""Спасибо за заказ. Подтвердите заказ по ссылке:
    http://127.0.0.1:8000/api/v1/confirmation/?u={activation_code}"""
    send_mail(
        'Подтверждение заказа',
        message,
        'test@mysite.com',
        [user, ]
    )
