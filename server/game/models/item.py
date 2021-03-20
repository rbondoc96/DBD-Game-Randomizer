from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from PIL import Image

from game.storage import OverwriteStorage

def item_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    subdir = str(instance.type).lower()
    return f"items/{subdir}/{filename}"

def overlay_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"overlays/items/{filename}"

class Item(models.Model):

    class Meta:
        ordering = ["type"]


    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey("game.ItemType", on_delete=models.CASCADE)
    rarities = models.ManyToManyField(
        "game.Rarity",
        verbose_name="Rarities",
        blank=True,
    )
    base_charges = models.IntegerField(
        verbose_name="Base Charges",
        default=8,
        validators=[MinValueValidator(0)]
    )
    description = models.TextField(null=True, blank=True)
    effects = models.ManyToManyField(
        "game.Effect", 
        verbose_name="Effects",
        blank=True)
    flavor = models.CharField(max_length=255, blank=True, null=True)
    
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
        super(Item, self).save(*args, **kwargs)      

        if self.overlay:
            image = Image.open(self.overlay)
            width, height = image.size
            if (width != 256) or (height != 256):
                image = image.resize((256, 256), Image.ANTIALIAS)
                image.save(self.overlay.path)            