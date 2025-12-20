from django.conf import settings
from django.core.mail import send_mail


class SendEmail:
    def __init__(self, subject, message, to_email):
        self.subject = subject
        self.message = message
        self.from_email = settings.EMAIL_HOST_USER
        self.to_email = to_email

    def send(self):
        try:
            send_mail(self.subject, self.message, self.from_email, [self.to_email])
            print("Email enviado com sucesso!", self.to_email)
            return True
        except Exception as e:
            print(e)
            return False
