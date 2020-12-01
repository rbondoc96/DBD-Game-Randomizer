from random import randint

from django.db import models
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from game.models import (
    Character,
    Perk,
    Power, PowerAddOn,
    Item, ItemAddOn,
    Effect,
    Offering,
)

def generate_player_id():
    return get_random_string(length=8).upper()

class Player(models.Model):
    class Role(models.TextChoices):
        SURVIVOR = "Survivor", _("Survivor")
        KILLER = "Killer", _("Killer")

    player_id = models.CharField(
        max_length=8,
        unique=True,
        verbose_name="Player ID",
        default=generate_player_id,
    )
    name = models.CharField(
        max_length=255, 
        verbose_name="Player Name",
        blank=True,
        null=True,
    )
    
    role = models.CharField(choices=Role.choices, max_length=15)    
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    offering = models.ForeignKey(
        Offering, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
    )
    item = models.ForeignKey(
        Item, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    power = models.ForeignKey(
        Power, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    item_addons = models.ManyToManyField(ItemAddOn, blank=True)
    power_addons = models.ManyToManyField(PowerAddOn, blank=True)
    perks = models.ManyToManyField(Perk)
    effects = models.ManyToManyField(Effect, blank=True)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ["player_id"]

    def __str__(self):
        if self.name:
            return f"Player {self.player_id}: {self.name}"
        else:
            return f"Player {self.player_id}"

    def clean(self, *args, **kwargs):
        if self.character.type != self.role:
            raise ValidationError("Character Type and Player Role must match.")

        if self.offering.type != self.role and self.offering.type != "All":
            raise ValidationError(
                "The Offering does not match the Player's Role"
            )

        super(Player, self).clean(*args, **kwargs)