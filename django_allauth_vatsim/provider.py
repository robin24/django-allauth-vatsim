from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from .views import VATSIMOAuth2Adapter

class VATSIMAccount(ProviderAccount):
    pass

class VATSIMProvider(OAuth2Provider):
    id = "vatsim"
    name = "VATSIM"
    account_class = VATSIMAccount
    oauth2_adapter_class = VATSIMOAuth2Adapter

    def extract_uid(self, data):
        return str(data["data"]["cid"])

    def get_default_scope(self):
        return [
            "full_name",
            "email",
            "vatsim_details",
            ]

    def extract_common_fields(self, data):
        personal = data["data"]["personal"]
        return dict(
            email=personal["email"],
            first_name=personal["name_first"],
            last_name=personal["name_last"],
            username=personal["name_first"].lower() + "_" + personal["name_last"].lower(),
        )

providers.registry.register(VATSIMProvider)