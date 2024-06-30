import datetime
import smtplib

import pytz
from django.core.mail import send_mail

from config import settings
from mailing.models import Mailing, Attempt


def send_message(mailing):
    subject = mailing.message.subject
    message = mailing.message.text
    try:
        response = send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.clients.all()],
            fail_silently=False,
        )
        if response == 1:

            mailing.status = 'IN_PROGRESS'
            server_response = 'Успешно отправлено'
            Attempt.objects.create(
                status=Attempt.ATTEMPT_SUCCESS, response=server_response, mailing=mailing)

            if mailing.periodicity == 'DAILY':
                mailing.start_mailing += datetime.timedelta(days=1)
            elif mailing.periodicity == 'WEEKLY':
                mailing.start_mailing += datetime.timedelta(days=7)
            elif mailing.periodicity == 'MONTHLY':
                mailing.start_mailing += datetime.timedelta(days=30)

            mailing.save()

    except smtplib.SMTPException as error:

        Attempt.objects.create(status=Attempt.ATTEMPT_FAIL, response=error, mailing=mailing)


def send_scheduled_mail():
    current_datetime = datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))

    for mailing in Mailing.objects.filter(status='IN_PROGRESS').filter(end_mailing__lt=current_datetime):
        mailing.status = 'COMPLETED'
        mailing.save()

    mailings = Mailing.objects.filter(status__in=['CREATED', 'IN_PROGRESS']).filter(start_mailing__lte=current_datetime)
    for mailing in mailings:
        mailing.status = 'IN_PROGRESS'
        mailing.save()
        send_message(mailing)
    print('Mailing completed')
