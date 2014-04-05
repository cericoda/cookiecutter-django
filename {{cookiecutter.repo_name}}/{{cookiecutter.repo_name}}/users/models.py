# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Import the basic Django ORM models library
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from allauth.account.signals import user_logged_in


# Subclass AbstractUser
class User(AbstractUser):

    def __unicode__(self):
        return self.username

def notify_login(sender, user, request, **kwargs):
    if user.id <> 1 and not settings.DEBUG:
        body = """Hi, \n
User %s (%s %s) Logged in \n
Referrer: %s
Remote_address: %s
HTTP_USER_AGENT: %s\n
they logged in to: %s (%s)\n
Regards

{{cookiecutter.repo_name}}""" % (user, 
               user.first_name, 
               user.last_name, 
               request.META['HTTP_REFERER'], 
               request.META['REMOTE_ADDR'], 
               request.META['HTTP_USER_AGENT'],
               request.META['SERVER_NAME'],
               request.META['HTTP_HOST'],
               )
        admin_emails = [v for k,v in settings.ADMINS]
        send_mail('%s logged in to {{cookiecutter.repo_name}}' % user, body, '{{cookiecutter.email}}',
                  admin_emails, fail_silently=True)

user_logged_in.connect(notify_login)
