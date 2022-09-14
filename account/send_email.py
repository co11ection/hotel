from django.core.mail import send_mail
from rooms.models import Rooms

def send_confirmation_email(user):
    code = user.activation_code
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
    to_email = user.email
    send_mail('Hello, please activate your account', f'to activate your account you need to follow the link {full_link}', 'j0hnsn0w003@gmail.com', [to_email], fail_silently=False)


def send_reset_password(user):
    code = user.activation_code
    to_email = user.email
    send_mail(
        'Hi'
        f'Your code for reset password: {code}',
        'j0hnsn0w003@gmail.com',
        [to_email,],
        fail_silently=False
    )

def send_notification(user, id):
    to_email = user.email
    send_mail(
        'уведомление о создании заказа',
        f'Вы создали заказ № {id}б ожидайте звонка',
        'from@example.com',
        [to_email,],
        fail_silently=False

    )

def send_html_email():
    from django.template.loader import render_to_string
    product = Rooms.objects.all()[0]
    html_message = render_to_string('f.html', {'name': product.title, 'description': product.description})
    send_mail(
        'subject',
        'Vam pismo',
        'lol.@gmail.com',
        ['tima.j.zh@gmail.com'],
        html_message=html_message,
        fail_silently=False
    )