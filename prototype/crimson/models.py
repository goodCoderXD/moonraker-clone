from django.db import models

# Game Components


class Player(models.Model):
    """Stats of a current player."""



class Action(models.Model):
    """Either a crew member or a action card."""
    is_crew = models.BooleanField(default=False)

    damage_provided = models.IntegerField(default=0)
    defense_provided = models.IntegerField(default=0)
    thruster_provided = models.IntegerField(default=0)
    reactor_provided = models.IntegerField(default=0)

class ShipUpgrade(models.Model):
    """A component that applies to the ship."""


class Contract(models.Model):
    """A mission players can do."""

    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(blank=True, null=True)

    playable = models.BooleanField(default=True) # For when you want to disable a contract

    paywalled_by = models.ManyToManyField(blank=True, to="Purchase", related_name="unlocked_contracts")

    # Contract Requirements
    damage_requirement = models.IntegerField(default=0)
    defense_requirement = models.IntegerField(default=0)
    thruster_requirement = models.IntegerField(default=0)
    reactor_requirement = models.IntegerField(default=0)
    crew_requirement = models.IntegerField(default=0)
    risk_dice = models.IntegerField(default=0)

    # Contract Rewards
    prestige_rewards = models.IntegerField(default=0)
    credit_rewards = models.IntegerField(default=0)
    draw_rewards = models.IntegerField(default=0)
