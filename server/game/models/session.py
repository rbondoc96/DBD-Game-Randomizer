from django.db import models
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

def generate_session_id():
    return get_random_string(length=6).upper()

class Session(models.Model):
    
    class GameMode(models.TextChoices):
        killer = "Killer", _("Killer")
        survivor = "Survivor", _("Survivor")
        custom = "Custom", _("Custom")
    
    session_id = models.CharField(
        max_length=6, 
        unique=True,
        verbose_name="Session ID",
        default=generate_session_id,
    )
    host = models.OneToOneField(
        "game.Player", 
        related_name="host", 
        on_delete=models.CASCADE,
    )

    mode = models.CharField(max_length=255, choices=GameMode.choices)
    players = models.ManyToManyField(
        "game.Player", 
        related_name="sessions",
        blank=True,
    )

    realm = models.ForeignKey(
        "game.Realm",
        verbose_name="Realm",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    obsession = models.ForeignKey(
        "game.Player", 
        related_name="obsession",
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
    )

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"Session {self.session_id}"