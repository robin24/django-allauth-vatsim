from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from django.conf import settings


class VATSIMOAuth2Adapter(OAuth2Adapter):
    provider_id = "vatsim"
    access_token_url = f"{settings.VATSIM_OAUTH_URL}/oauth/token"
    authorize_url = f"{settings.VATSIM_OAUTH_URL}/oauth/authorize"
    profile_url = f"{settings.VATSIM_OAUTH_URL}/api/user"

    def complete_login(self, request, app, token, **kwargs):
        headers = {
            "Authorization": f"Bearer {token.token}",
                   }
        metadata = (
            get_adapter().get_requests_session().get(self.profile_url, headers=headers)
        )
        extra_data = metadata.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(VATSIMOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(VATSIMOAuth2Adapter)