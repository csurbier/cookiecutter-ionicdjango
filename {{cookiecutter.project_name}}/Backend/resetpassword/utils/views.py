# -*-coding:utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from {{cookiecutter.project_name}}.settings import DEFAULT_FROM_EMAIL
from django.views.generic import *
from .forms import SetPasswordForm
from django.contrib import messages
#from django.contrib.auth.models import User
from bo.models import AppUser
from django.http import HttpResponse
import hashlib
from django.shortcuts import render
import sendgrid
import logging
from django.views.decorators.csrf import csrf_exempt
import os
from bo.signals import envoiMessageMail
from sendgrid.helpers.mail import Mail,Email,Content

from sendgrid import SendGridAPIClient
from {{cookiecutter.project_name}} import settings
logger = logging.getLogger('django')

def reset_password(user, request):
    print("On recoit demande========")
    c = {
        'email': user.email,
        'domain': request.META['HTTP_HOST'],
        'site_name': '{{cookiecutter.project_name}}',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
        'user': user,
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
    }
    print("PK UID %s"%user.pk)
    subject_template_name = 'registration/password_reset_subject.txt'
    # copied from
    # django/contrib/admin/templates/registration/password_reset_subject.txt
    # to templates directory
    email_template_name = 'registration/password_reset_email.html'
    # copied from
    # django/contrib/admin/templates/registration/password_reset_email.html
    # to templates directory
    subject = loader.render_to_string(subject_template_name, c)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    email = loader.render_to_string(email_template_name, c)
    print("On fait demande ENVOI MAIL ======== %s" % user.email)
    try:
        to_email = Email(user.email)
        from_email = Email({{cookiecutter.emailContact}})
        content = Content('text/html', email)
        message = Mail(from_email, subject, to_email, content)
        sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=message.get())
        logger.info("[SMTP] status code %s" % response.status_code)
        logger.info("[SMTP] body %s" % response.body)
        logger.info("[SMTP] headers %s" % response.headers)
    except Exception as e:
        logger.info(e.message)
    #send_mail(subject, email, DEFAULT_FROM_EMAIL,[user.email], fail_silently=False)


@csrf_exempt
def sendPasswordLink(request):
    if request.method == "POST":
        data = request.POST['email_or_username']
        associated_users = AppUser.objects.filter(email=data)
        try:
         if associated_users.exists():
                for user in associated_users:
                    reset_password(user, request)
                return HttpResponse(status=200)
        except Exception as e:
                logger.info(e)
        return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)
@csrf_exempt
def sendValidateLink(request):
    if request.method == "POST":
        data = request.POST['email']
        user = AppUser.objects.get(email=data)
        try:
         if user:
            #print("On recoit demande========")
            c = {
                 'email': user.email,
                 'domain': request.META['HTTP_HOST'],
                 'site_name': '{{cookiecutter.project_name}}',
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
                 'user': user,
                 'token': default_token_generator.make_token(user),
                 'protocol': 'http',
             }
            logger.info("PK UID %s" % user.pk)
            #subject_template_name = 'registration/validate_account_subject.txt'
             # copied from
             # django/contrib/admin/templates/registration/password_reset_subject.txt
             # to templates directory
            email_template_name = 'registration/validate_account_email.html'
             # copied from
             # django/contrib/admin/templates/registration/password_reset_email.html
             # to templates directory
            subject = "{{cookiecutter.project_name}} : Validation de ton compte"
             # Email subject *must not* contain newlines
            #subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)

            logger.info("On fait demande ENVOI MAIL ======== %s " % (user.email))

            to_email = Email(user.email)
            from_email = Email({{cookiecutter.emailContact}})
            content = Content('text/html', email)
            message = Mail(from_email, subject, to_email, content)
            sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
            response = sg.client.mail.send.post(request_body=message.get())
            logger.info("[SMTP] status code %s" % response.status_code)
            logger.info("[SMTP] body %s" % response.body)
            logger.info("[SMTP] headers %s" % response.headers)
            return HttpResponse(status=200)
        except Exception as e:
                logger.error(e)
        return HttpResponse(status=404)
    else:
        return HttpResponse(status=500)

def pwdenvoye(request):
    return render(request,'account/pwdmodifie.html',{})

class PasswordResetConfirmView(FormView):
    template_name = "account/pwdoublie.html"
    success_url = '/account/pwdenvoye'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            import base64
            uid = base64.b64decode(uidb64).decode('utf-8')
           # import uuid
            #identifiant = uuid.UUID(bytes=uid)
            print("uid user %s" % (uid))
            user = AppUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, AppUser.DoesNotExist) as e:
            user = None
            print(e)
            print("Utilisateur doesnt exist")

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['confirmation']

                user.password = hashlib.sha256(new_password.encode('utf8')).hexdigest()
                user.save()
                messages.success(request, 'Votre mot de passe a été modifié.')
                return self.form_valid(form)
            else:
                print(form.errors)
                messages.error(request, form.errors)
                return self.form_invalid(form)
        else:
            print("User %s"%user)
            messages.error(
                request, 'Ce lien a expiré. Merci de refaire une demande.')
            return self.form_invalid(form)

def validateAccount(request,uidb64,token):
    # get user uuid and get token in url
    assert uidb64 is not None and token is not None  # checked by URLconf
    logger.info("============== validateAccount %s %s"%(uidb64,token))

    try:
        uid = urlsafe_base64_decode(uidb64)
        logger.info("============== OK On cherche user %s"%(uid))
        user = AppUser.objects.get(pk=uid)
        user.valid = True
        user.save()
    except (TypeError, ValueError, OverflowError, AppUser.DoesNotExist):
        logger.info("============== User not exist")
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        return render(request, 'account/valid.html', {})
    else:
        return render(request, 'account/invalid.html', {})