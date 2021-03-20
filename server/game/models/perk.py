from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.db import models

from PIL import Image

from game.storage import OverwriteStorage

def perk_directory_path(instance, filename):
    filename = f"{instance.name}" + "." \
        + filename.split(".").pop()
    subdir = str(instance.type).lower()
    return f"perks/{subdir}/{filename}"

def overlay_directory_path(instance, filename):
    filename = f"{instance.name}" + "." \
        + filename.split(".").pop()
    subdir = str(instance.type).lower()
    return f"overlays/perks/{subdir}/{filename}"    

class Perk(models.Model):
    class Type(models.TextChoices):
        SURVIVOR = "Survivor", _("Survivor")
        KILLER = "Killer", _("Killer")

    class Tiers(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3

    class Meta:
        ordering = ["type", "name"]     

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(choices=Type.choices, max_length=15)
    owner = models.ForeignKey(
        "game.Character", 
        blank=True, 
        null=True,
        on_delete=models.CASCADE)

    rarities = models.ManyToManyField(
        "game.Rarity",
        verbose_name="Rarities",
        blank=True,
    )

    tiers = ArrayField(
        ArrayField(
            models.CharField(max_length=255, blank=True),
        ),
        size=3,
        blank=True,
        null=True,
    )

    description = models.TextField(null=True, blank=True)

    effects = models.ManyToManyField(
        "game.Effect", 
        verbose_name="Effects", 
        blank=True)
    
    flavor = models.CharField(max_length=255, null=True, blank=True)

    overlay = models.ImageField(
        upload_to=overlay_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )

    patch_version = models.CharField(
        max_length=11,
        verbose_name="Patch Version",
        null=True, blank=True)

    wiki_url = models.URLField(
        max_length=2000,
        verbose_name="Wiki Page",
        null=True, blank=True)


    def __str__(self):
        return f"[{self.type}] {self.name}"


    def save(self, *args, **kwargs):
        super(Perk, self).save(*args, **kwargs)
       

        if self.overlay:
            image = Image.open(self.overlay)
            width, height = image.size
            if (width != 256) or (height != 256):
                image = image.resize((256, 256), Image.ANTIALIAS)
                image.save(self.overlay.path)             