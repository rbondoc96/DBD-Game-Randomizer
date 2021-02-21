from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from PIL import Image

from game.storage import OverwriteStorage

def item_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    subdir = str(instance.type).lower()
    return f"items/{subdir}/{filename}"

def template_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"templates/items/{filename}"

class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey("game.ItemType", on_delete=models.CASCADE)
    rarity = models.ForeignKey(
        "game.Rarity", 
        null=True, 
        on_delete=models.SET_NULL
    )
    base_charges = models.IntegerField(
        verbose_name="Base Charges",
        default=8,
        validators=[MinValueValidator(0)]
    )
    description = models.TextField()
    effects = models.ManyToManyField("game.Effect", verbose_name="Effects")
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
        

        
