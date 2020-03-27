# *coding: utf-8*
from __future__ import unicode_literals
from django.db import models
from swiitch import settings
from django.db.models.signals import pre_delete,post_save,post_delete,pre_save
from bo.signals import *
#from bo.helpers import *
from PIL import Image
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
import uuid
from django.utils import timezone
from tinymce.models import HTMLField

class AppUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=100,unique=False)
    password = models.CharField(max_length=255)
    firstName = models.CharField(max_length=100, null=True, blank=True)
    facebookId = models.CharField(max_length=100, null=True, blank=True)
    googleId = models.CharField(max_length=100, null=True, blank=True)
    appleId = models.TextField(null=True, blank=True)
    lastConnexionDate = models.DateTimeField(null=True, blank=True)
    valid = models.BooleanField(default=True)
    connection_choice = (
        (0, "ios"),
        (1, "android"),
        (2, "web"),
    )
    connectionType= models.IntegerField(choices=connection_choice, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    @property
    def last_login(self):
        return self.lastConnexionDate

    def __str__(self):
        return u'%s' % (self.email)

  
 

class AppleSignIn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.TextField(null=True, blank=True)
    token = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    jsonUser = models.TextField(null=True,blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u'%s - %s' % (self.code,self.state)

class NotificationToSend(models.Model):
    toUserId = models.ForeignKey('AppUser', db_index=True,related_name="toUser",on_delete=models.CASCADE)
    message = models.CharField(max_length=1024,null=True,blank=True)
    extra = models.CharField(max_length=10,default="",null=True,blank=True)
    notif_type_choice = (
        (0, "PUSH"),
        (1, "EMAIL"),
    )
    notifyType = models.IntegerField(choices=notif_type_choice)
    status_choice = (
        (0, "TO_SEND"),
        (1, "SENDING"),
        (2, "SENT"),
        (3, "ERROR_SENDING"),
        (4, "NO_PUSH_TOKEN"),
    )
    status = models.IntegerField(choices=status_choice)
    sendStatus = models.TextField(null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-createdAt', ]

    def __str__(self):
        return u'%s' % (self.toUserId)