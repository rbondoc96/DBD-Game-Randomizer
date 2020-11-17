from django.utils.translation import gettext_lazy as _
from django.db import models

from PIL import Image

from game.storage import OverwriteStorage

def character_directory_path(instance, filename):
    # Note the "s" at the end making it plural
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"characters/{instance.type}s/{filename}"

class Character(models.Model):
    class Type(models.TextChoices):
        SURVIVOR = "Survivor", _("Survivor")
        KILLER = "Killer", _("Killer")

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(choices=Type.choices, max_length=15)     
    
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
        return f"[{self.type}] {self.name}"  

    def save(self, *args, **kwargs):
        super(Character, self).save(*args, **kwargs)
        
        if self.image:
            image = Image.open(self.image)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.image.path)
