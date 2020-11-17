from django.utils.translation import gettext_lazy as _
from django.db import models

from PIL import Image

from game.storage import OverwriteStorage
from game.models import Rarity, Effect, Character

def perk_directory_path(instance, filename):
    filename = f"{instance.name}{instance.tier}" + "." \
        + filename.split(".").pop()
    subdir = str(instance.type).lower()
    return f"perks/{subdir}/{filename}"

def template_directory_path(instance, filename):
    filename = f"{instance.name}{instance.tier}" + "." \
        + filename.split(".").pop()
    subdir = str(instance.type).lower()
    return f"templates/perks/{subdir}/{filename}"    

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

    # Template overlay that will be put overlay the bg+border layer 
    # May or may not be transparent bg
    template = models.ImageField(
        upload_to=template_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )

    # Converted icon
    image = models.ImageField(
        upload_to=perk_directory_path, 
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["type", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "tier"],
                name="perk_name_tier_key"
            )
        ]

    def __str__(self):
        return f"[{self.type}] {self.name} - Tier {self.tier}"

    def save(self, *args, **kwargs):
        super(Perk, self).save(*args, **kwargs)
        
        if self.image:
            image = Image.open(self.image)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.image.path)        

        if self.template:
            image = Image.open(self.template)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.template.path)            