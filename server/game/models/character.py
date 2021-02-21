from django.utils.translation import gettext_lazy as _
from django.db import models

from PIL import Image

from game.storage import OverwriteStorage

def character_directory_path(instance, filename):
    # Note the "s" at the end making it plural
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"characters/{instance.type}s/{filename}"

def template_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"templates/characters/{filename}"

class Character(models.Model):
    class Type(models.TextChoices):
        SURVIVOR = "Survivor", _("Survivor")
        KILLER = "Killer", _("Killer")

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(choices=Type.choices, max_length=15)
    is_licensed = models.BooleanField(
        default=False,
        verbose_name="Licensed Character?"
    )     
    
    # Template overlay that will be put overlay the bg+border layer 
    # May or may not be transparent bg
    template = models.ImageField(
        upload_to=template_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )

    # Storage allows for existing images to be overwritten
    image = models.ImageField(
        upload_to=character_directory_path, 
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["type", "name"]

    def __str__(self):
        return f"{self.name}"  

    def save(self, *args, **kwargs):
        super(Character, self).save(*args, **kwargs)            
