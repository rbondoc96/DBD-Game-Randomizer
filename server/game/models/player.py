from random import randint

from django.db import models
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
        default="Player",
    )
    
    role = models.CharField(
        choices=Role.choices, 
        max_length=15, 
        null=True,
        blank=True,
    )    
    character = models.ForeignKey(
        "game.Character", 
        on_delete=models.CASCADE, 
        null=True,
        blank=True,
    )
    offering = models.ForeignKey(
        "game.Offering", 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
    )
    item = models.ForeignKey(
        "game.Item", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    power = models.ForeignKey(
        "game.Power", 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    item_addons = models.ManyToManyField("game.ItemAddOn", blank=True)
    power_addons = models.ManyToManyField("game.PowerAddOn", blank=True)
    perks = models.ManyToManyField("game.Perk", blank=True)
    # effects = models.ManyToManyField("game.Effect", blank=True)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ["created", "player_id"]

    def __str__(self):
        return f"{self.name}#{self.player_id}"

    def clean(self, *args, **kwargs):
        if self.character and self.role:
            if self.character.type != self.role:
                raise ValidationError(
                    "Character Type and Player Role must match."
                )

        if self.offering and self.role:
            if self.offering.type != self.role and self.offering.type != "All":
                raise ValidationError(
                    "Offering does not match the Player's Role"
                )

        super(Player, self).clean(*args, **kwargs)