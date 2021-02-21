from django.db import models
from django.utils.translation import gettext_lazy as _

from PIL import Image

from game.storage import OverwriteStorage

def offering_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    subdir = str(instance.type).lower()
    return f"offerings/{subdir}/{filename}"

def template_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    subdir = str(instance.type).lower()
    return f"templates/offerings/{subdir}/{filename}"    

class Offering(models.Model):
    class Type(models.TextChoices):
        SURVIVOR = "Survivor", _("Survivor")
        KILLER = "Killer", _("Killer")
        ALL = "All", _("All")
        
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(
        choices=Type.choices, 
        max_length=15, 
        default=Type.ALL)
    rarity = models.ForeignKey("game.Rarity", on_delete=models.CASCADE)
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

    # Composed image    
    image = models.ImageField(
        upload_to=offering_directory_path, 
        storage=OverwriteStorage(),
        blank=True,
        null=True
    ) 

    class Meta:
        ordering = ["type"]   
    
    def __str__(self):
        return f"[{self.type}] {self.name}"

    def save(self, *args, **kwargs):
        super(Offering, self).save(*args, **kwargs)
        
        if self.image:
            image = Image.open(self.image)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.image.path)          

        if self.template:
            image = Image.open(self.template)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.template.path)            