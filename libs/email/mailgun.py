from django.core.mail import send_mail, EmailMessage


class EmailClient(object):

    def send_mail(self, subject, body, from_email, recipient_list):
        send_mail(subject, body, from_email, recipient_list)
