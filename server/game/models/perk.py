from django.utils.translation import gettext_lazy as _
from django.db import models

from game.models import Rarity, Effect, Character

class Perk(models.Model):
    class Type(models.TextChoices):
        SURVIVOR = "Survivor", _("Survivor")
        KILLER = "Killer", _("Killer")

    class Tiers(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3

    name = models.CharField(max_length=255)
    type = models.CharField(choices=Type.choices, max_length=15)
    owner = models.ForeignKey(
        Character, 
        blank=True, 
        null=True,
        on_delete=models.CASCADE)
    tier = models.IntegerField(choices=Tiers.choices)
    rarity = models.ForeignKey(Rarity, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    effects = models.ManyToManyField(Effect, verbose_name="Effects")
    quote = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "tier"],
                name="perk_name_tier_key"
            )
        ]

    def __str__(self):
        return f"{self.name} - Tier {self.tier}"