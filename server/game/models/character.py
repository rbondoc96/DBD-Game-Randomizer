from django.utils.translation import gettext_lazy as _
from django.db import models

from PIL import Image

from game.storage import OverwriteStorage

def character_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"characters/{instance.type}s/{filename}"

class Character(models.Model):
    class Type(models.TextChoices):
        SURVIVOR = "Survivor", _("Survivor")
        KILLER = "Killer", _("Killer")

    class Meta:
        ordering = ["type", "name"]        

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(choices=Type.choices, max_length=15)
    is_licensed = models.BooleanField(
        default=False,
        verbose_name="Licensed Character?"
    )     

    image = models.ImageField(
        upload_to=character_directory_path, 
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )

    wiki_url = models.URLField(
        max_length=2000,
        verbose_name="Wiki Page",
        null=True, blank=True)    


    def __str__(self):
        return f"[{self.type}] {self.name}"

    def get_name(self):
        return self.name
