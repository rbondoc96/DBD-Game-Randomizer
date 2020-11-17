from django.db import models

from PIL import Image

from game.storage import OverwriteStorage
from game.models import Rarity, Effect, Character

def power_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"powers/{filename}"

def template_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"templates/powers/{filename}"    

class Power(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(Character,on_delete=models.CASCADE, null=True)
    description = models.TextField()
    effects = models.ManyToManyField(Effect, verbose_name="Effects")

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
        upload_to=power_directory_path, 
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )    

    def __str__(self):
        return f"[{self.owner.name}] {self.name}"

    def save(self, *args, **kwargs):
        super(Power, self).save(*args, **kwargs)
        
        if self.image:
            image = Image.open(self.image)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.image.path)  

        if self.template:
            image = Image.open(self.template)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.template.path)                    
    
    class Meta:
        ordering = ["owner"]
        

        
