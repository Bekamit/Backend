from django.core.mail import send_mail


def send_confirmation_email(email, code):
    send_mail(
        'Здраствуйте активируйте ваш аккаунт',
        f'Что бы активировать ваш аккаунтт скопируйте и введите на сайте код:'
        f'\n{code}'
        f'\n не передавайте его никому',
        'sadyr.top@gmail.com',
        [email],
        fail_silently=False
    )