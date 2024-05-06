from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.contrib.auth.models import Group
from accounts.models import UserProfile


class VATSIMSocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        """Save the user and add them to the VATSIM group."""
        user = super().save_user(request, sociallogin, form)
        # Create the user profile
        cid = sociallogin.account.extra_data.get("data").get("cid")
        data = sociallogin.account.extra_data.get("data").get("vatsim")
        profile, created = UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "cid": cid,
                "rating_id": data.get("rating").get("id"),
                "rating_long": data.get("rating").get("long"),
                "rating_short": data.get("rating").get("short"),
                "region_id": data.get("region").get("id"),
                "region_name": data.get("region").get("name"),
                "division_id": data.get("division").get("id"),
                "division_name": data.get("division").get("name"),
                "pilot_rating_id": data.get("pilotrating").get("id"),
                "pilot_rating_long": data.get("pilotrating").get("long"),
                "pilot_rating_short": data.get("pilotrating").get("short"),
                "subdivision_id": data.get("subdivision").get("id"),
                "subdivision_name": data.get("subdivision").get("name"),
            }
        )

        # Get or create the VATSIM group
        group, created = Group.objects.get_or_create(name="VATSIM")
        # Add the user to the VATSIM group
        user.groups.add(group)
        return user