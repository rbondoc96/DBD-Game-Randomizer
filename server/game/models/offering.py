from django.db import models
from django.utils.translation import gettext_lazy as _

from PIL import Image

from game.storage import OverwriteStorage

def offering_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    subdir = str(instance.type).lower()
    return f"offerings/{subdir}/{filename}"

def overlay_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    subdir = str(instance.type).lower()
    return f"overlays/offerings/{subdir}/{filename}"    

class Offering(models.Model):
    class Type(models.TextChoices):
        SURVIVOR = "Survivor", _("Survivor")
        KILLER = "Killer", _("Killer")
        ALL = "All", _("All")

    class Meta:
        ordering = ["type"]          
        
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(
        choices=Type.choices, 
        max_length=15, 
        default=Type.ALL)
    rarity = models.ForeignKey("game.Rarity", on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    effects = models.ManyToManyField(
        "game.Effect", 
        verbose_name="Effects",
        blank=True)
    quote = models.CharField(max_length=255, blank=True, null=True)

    overlay = models.ImageField(
        upload_to=overlay_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to=offering_directory_path, 
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
        super(Offering, self).save(*args, **kwargs)
        
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