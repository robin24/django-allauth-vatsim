from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import VATSIMProvider

urlpatterns = default_urlpatterns(VATSIMProvider)