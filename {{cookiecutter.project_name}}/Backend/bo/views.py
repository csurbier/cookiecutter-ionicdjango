from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from bo.models import *
from urllib.parse import urlparse

from django.shortcuts import redirect, render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.template import loader
from django.middleware.csrf import get_token
import requests
import logging

# Get an instance of a logger
logger = logging.getLogger('django')
def index(request):
    return render(request, 'bo/maundy/index.html')


def cgu(request):
    return  render(request, 'bo/cgu.html', {})

def appleCode(request):
    data = request._data
    token = data['token']
    pass
