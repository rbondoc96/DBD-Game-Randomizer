from django.utils.translation import gettext_lazy as _
from django.db import models

class Character(models.Model):
    class Type(models.TextChoices):
        SURVIVOR = "Survivor", _("Survivor")
        KILLER = "Killer", _("Killer")

    name = models.CharField(max_length=255)
    type = models.CharField(choices=Type.choices, max_length=15)     
    
    # Image uploaded to /media/characters since MEDIA_ROOT is set
    image = models.ImageField(upload_to="characters", null=True)

    def __str__(self):
        return f"[{self.type}] {self.name}"  