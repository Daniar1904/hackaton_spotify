from django.core.mail import send_mail

def send_confirmation_email(user, code):
    print('send_conf_mail_worked')
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}/'
    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Чтобы активировать ваш аккаунт нужно перейти по ссылке: \n{full_link}',
        'kazakovdaniar2002@gmail.com',
        [user],
        fail_silently=False
    )