from django.db import models

from PIL import Image

from game.storage import OverwriteStorage
from game.models import Rarity, Effect

def item_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    subdir = str(instance.type).lower()
    # Note the "s" making it plural
    return f"items/{subdir}s/{filename}"

def template_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"templates/items/{filename}"

class ItemType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Item Type"
        verbose_name_plural = "Item Types"

class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    rarity = models.ForeignKey(Rarity, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    effects = models.ManyToManyField(Effect, verbose_name="Effects")
    quote = models.CharField(max_length=255, blank=True, null=True)
    
    # Template overlay that will be put overlay the bg+border layer 
    # May or may not be transparent bg
    template = models.ImageField(
        upload_to=template_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )

    # Composed image after the template overlay is merged with the bg+border
    image = models.ImageField(
        upload_to=item_directory_path, 
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )    

    def __str__(self):
        return f"[{self.type}] {self.name}"

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)
        
        if self.image:
            image = Image.open(self.image)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.image.path)          

        if self.template:
            image = Image.open(self.template)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.template.path)               
    
    class Meta:
        ordering = ["type"]
        

        
