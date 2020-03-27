"""flip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from bo.views import index,cgu,registerUber,appleCode
from django.conf.urls.static import static
from django.conf import settings
from resetpassword.utils.views import PasswordResetConfirmView,sendPasswordLink,pwdenvoye,sendValidateLink,validateAccount
from django.conf import settings

from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path(".well-known/apple-developer-domain-association.txt", RedirectView.as_view(url=staticfiles_storage.url("apple-developer-domain-association.txt")), ),
              path("loaderio-1eec92d04539c93c5cf80a7fbe1e9ad4.txt", RedirectView.as_view(
                      url=staticfiles_storage.url("loaderio-1eec92d04539c93c5cf80a7fbe1e9ad4.txt")), ),

                  path('', index),
    #path('', include(router.urls)),
    path('backoffice/', admin.site.urls),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    re_path('account/reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)',
                          PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account/reset_password', sendPasswordLink, name="reset_password"),
    path('account/validate_account', sendValidateLink, name="validate_link"),
    re_path('account/validate_account_confirm/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)',
                          validateAccount, name='validate_account_confirm'),
    path('account/pwdenvoye', pwdenvoye, name="pwdenvoye"),
    path('docs/', include('rest_framework_docs.urls')),
    path('api/', include('api.urls')),
    path('o/', include('oauth2_provider.urls')),
    path('',index),
    path('cgu/', cgu),
    path('uber/oauth/connect/', registerUber),
    path('tinymce/', include('tinymce.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


