from django.utils.translation import gettext_lazy as _
from django.db import models

from PIL import Image

from game.storage import OverwriteStorage

def perk_directory_path(instance, filename):
    filename = f"{instance.name}{instance.tier}" + "." \
        + filename.split(".").pop()
    subdir = str(instance.type).lower()
    return f"perks/{subdir}/{filename}"

def overlay_directory_path(instance, filename):
    filename = f"{instance.name}{instance.tier}" + "." \
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
        constraints = [
            models.UniqueConstraint(
                fields=["name", "tier"],
                name="perk_name_tier_key"
            )
        ]        

    name = models.CharField(max_length=255)
    type = models.CharField(choices=Type.choices, max_length=15)
    owner = models.ForeignKey(
        "game.Character", 
        blank=True, 
        null=True,
        on_delete=models.CASCADE)
    tier = models.IntegerField(choices=Tiers.choices)
    rarity = models.ForeignKey(
        "game.Rarity", 
        null=True, 
        on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    effects = models.ManyToManyField(
        "game.Effect", 
        verbose_name="Effects", 
        blank=True)
    quote = models.CharField(max_length=255, null=True, blank=True)

    overlay = models.ImageField(
        upload_to=overlay_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to=perk_directory_path, 
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
        return f"[{self.type}] {self.name} - Tier {self.tier}"


    def save(self, *args, **kwargs):
        super(Perk, self).save(*args, **kwargs)
        
        if self.image:
            image = Image.open(self.image)
            width, height = image.size
            if (width != 256) or (height != 256):
                image = image.resize((256, 256), Image.ANTIALIAS)
                image.save(self.image.path)        

        if self.overlay:
            image = Image.open(self.overlay)
            width, height = image.size
            if (width != 256) or (height != 256):
                image = image.resize((256, 256), Image.ANTIALIAS)
                image.save(self.overlay.path)             