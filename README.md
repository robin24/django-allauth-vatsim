# django-allauth-vatsim
OAuth2 login provider for VATSIM using django-allauth.

## Description

Welcome to django-allauth-vatsim!

This OAuth2 provider for [django-allauth](https://github.com/pennersr/django-allauth/) enables users to log in using their account on the [VATSIM](https://vatsim.net) online ATC network.
The following components are included:

* OAuth2 provider for VATSIM (supports both production and sandbox environments).
* Social account adapter which can optionally be used to populate the user model with VATSIM-specific account details, such as a user's CID, pilot / controller rating and ATC division.
* Implementation of a basic test case to ensure that the login provider works as expected.

## Installation
To get started, install and configure django-allauth as described [here](https://docs.allauth.org/en/latest/installation/index.html).
Next, install django-allauth-vatsim into your project.
```
pip install django-allauth-vatsim
```
In your settings.py file, add it to your INSTALLED_APPS list so it looks similar to this:
```
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # 3rd party apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_allauth_vatsim",
]
```
Also, add the base VATSIM OAuth2 URL:

* For the sandbox environment, use https://auth-dev.vatsim.net.
* For the production server, use https://auth.vatsim.net.

The corresponding line in your settings.py file should look like the following:
```
VATSIM_OAUTH_URL = "https://auth.vatsim.net"
```

Finally, you need to configure the credentials (client ID and secret) which you have obtained from VATSIM. As these are sensitive credentials, it is highly recommended to store them as environment variables using a package such as [environs](https://pypi.org/project/environs/).
The provider configuration should be specified as follows:
```
SOCIALACCOUNT_PROVIDERS = {
    "vatsim": {
        "APP": {
            "client_id": "<YOUR_CLIENT_ID>",
            "secret": "<YOUR_CLIENT_SECRET>",
        }
    },
}
```

Once all of the above is done, you can start using the new login provider, e.g. by using the following tag in your login template to initiate the authentication flow:
```
{% provider_login_url 'vatsim' %}
```

### Optional: adding the social account adapter to populate user profiles
If you like, you can utilize the included social account adapter to populate a user's profile in your database with additional details, such as their CID, VATSIM division, and controller / pilot rating information.

The adapter is configured to store this information in a Profile database model that is linked to the user model with a one-to-one relationship, which means it is also necessary to set up and configure a basic customized user model to make this work, preferably in a dedicated accounts app.
The steps required to set this up are beyond the scope of this README, but [this excellent tutorial](https://learndjango.com/tutorials/django-custom-user-model) will guide you through the process.
As an example, the CustomUser and UserProfile models that I created while working on this look as follows:
```
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    cid = models.IntegerField(primary_key=True)
    rating_id = models.IntegerField()
    rating_long = models.CharField(max_length=100)
    rating_short = models.CharField(max_length=50)
    region_id = models.CharField(max_length=20)
    region_name = models.CharField(max_length=100)
    division_id = models.CharField(max_length=20, blank=True, null=True)
    division_name = models.CharField(max_length=100, blank=True, null=True)
    pilot_rating_id = models.IntegerField()
    pilot_rating_long = models.CharField(max_length=100)
    pilot_rating_short = models.CharField(max_length=50)
    subdivision_id = models.CharField(max_length=20, blank=True, null=True)
    subdivision_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} {self.cid}"
```

If you decide to set this up in your project, add the following line to settings.py to register the social account adapter:
```
SOCIALACCOUNT_ADAPTER = "django_allauth_vatsim.adapter.VATSIMSocialAccountAdapter"
````

## Contributing

As this is my first time publishing a Python package and also my first time developing a plugin for django-allauth, it's very much possible that I've overlooked something obvious that could make this project even more stable and / or useful.
As such, contributions, suggestions and constructive criticisms are most welcome and greatly appreciated.
If you do encounter any issues or would like to improve this package, feel free to open an issue or submit a pull request.