from django.db import models
from django.contrib.auth.models import AbstractUser

# FWIW, Riot's Pricing:
# About $1 = 100 points
# $4.99 -> 575 RP (0 bonus)
# $10.99 -> 1275 (105 bonus)
# $21.99 -> 2525 (275 bonus)
# $34.99 -> 4025 (475 bonus)
# $49.99 -> 5750 (750 bonus)
# $99.99 -> 11525 (1975 bonus)


class Account(AbstractUser):
    """Expand the existing user object."""

    profile_picture = models.ImageField(blank=True, null=True)
    level = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)

    # If the email was verified
    verified = models.BooleanField(default=False)

    # The in game currency
    star_dust = models.IntegerField(default=100)

    # Items Purchased
    purchases = models.ManyToManyField(to="Purchase", related_name="owned_by")


class Purchase(models.Model):
    """Something Pay2Win, e.g. skins, etc."""

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    star_dust_cost = models.IntegerField(default=100)
