from django.core.mail import send_mail

def send_confirmation_email(user, code):
    full_link = f'http://localhost:8000/api/v1/users/activate/{code}/'
    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Чтобы активировать ваш аккаунт нужно перейти по ссылке: \n{full_link}',
        'kazakovdaniar2002@gmail.com',
        [user],
        fail_silently=False
    )