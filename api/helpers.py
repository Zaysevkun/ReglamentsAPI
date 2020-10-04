from django.core.mail import EmailMessage


def send_mail_to_department_users(departments):
    emails = list(departments.filter(users__allow_send_info_emails=True).values_list(
        'users__user__email', flat=True))
    if emails:
        subject = f"Вы назначены утвердителем регламента"
        body = ('Вы назначены утвердителем регламента. Тут должна быть ссылка на регламент,'
                'Кирилл, не забудь поставить!!')
        email = EmailMessage(subject, to=emails, body=body)
        email.send()
