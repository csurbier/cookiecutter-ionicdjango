from django.conf.urls import url
from rest_framework_docs.views import DRFDocsView,PartnerDocsView

urlpatterns = [
    # Url to view the API Docs
    url(r'^$', DRFDocsView.as_view(), name='drfdocs'),
    url(r'^partners', PartnerDocsView.as_view(), name='partnerdocs'),

]
