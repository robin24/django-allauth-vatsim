"""Test VATSIM OAuth2 Flow."""
from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase

from django_allauth_vatsim.provider import VATSIMProvider


class VATSIMProviderTests(OAuth2TestsMixin, TestCase):

    """Test Class for VATSIM OAuth2."""

    json_payload = """{
      "data": {
        "cid": "10000001",
        "oauth": {
          "token_valid": "true"
        },
        "vatsim": {
          "rating": {
            "id": 1,
            "long": "Pilot/Observer",
            "short": "OBS"
          },
          "region": {
            "id": "APAC",
            "name": "Asia Pacific"
          },
          "division": {
            "id": "PAC",
            "name": "Australia (VATPAC)"
          },
          "pilotrating": {
            "id": 0,
            "long": "New Member",
            "short": "NEW"
          },
          "subdivision": {
            "id": null,
            "name": null
          }
        },
        "personal": {
          "email": "auth.dev1@vatsim.net",
          "name_full": "Web One",
          "name_last": "One",
          "name_first": "Web"
        }
      }
    }"""

    provider_id = VATSIMProvider.id

    def get_mocked_response(self):
        """Test authentication flow."""
        return MockedResponse(
            200, self.json_payload)