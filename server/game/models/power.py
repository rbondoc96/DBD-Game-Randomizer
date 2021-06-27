from django.db import models

from PIL import Image

from game.storage import OverwriteStorage

def primary_power_directory_path(instance, filename):
    filename = f"{instance.name}-primary" + "." + filename.split(".").pop()
    return f"powers/{filename}"

def secondary_power_directory_path(instance, filename):
    filename = f"{instance.name}-secondary" + "." + filename.split(".").pop()
    return f"powers/{filename}"

def tertiary_power_directory_path(instance, filename):
    filename = f"{instance.name}-tertiary" + "." + filename.split(".").pop()
    return f"powers/{filename}"    

def primary_overlay_directory_path(instance, filename):
    filename = f"{instance.name}-primary" + "." + filename.split(".").pop()
    return f"overlays/powers/{filename}"    

def secondary_overlay_directory_path(instance, filename):
    filename = f"{instance.name}-secondary" + "." + filename.split(".").pop()
    return f"overlays/powers/{filename}"     

def tertiary_overlay_directory_path(instance, filename):
    filename = f"{instance.name}-tertiary" + "." + filename.split(".").pop()
    return f"overlays/powers/{filename}"    

class Power(models.Model):

    class Meta:
        ordering = ["owner"]

    name = models.CharField(max_length=255, unique=True)
    owner = models.OneToOneField(
        "game.Character",
        on_delete=models.CASCADE, 
        primary_key=False
    )
    description = models.TextField(null=True, blank=True)
    effects = models.ManyToManyField(
        "game.Effect", 
        verbose_name="Effects",
        blank=True)

    primary_overlay = models.ImageField(
        upload_to=primary_overlay_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )
    secondary_overlay = models.ImageField(
        upload_to=secondary_overlay_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )
    tertiary_overlay = models.ImageField(
        upload_to=tertiary_overlay_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )
       
    flavor = models.CharField(max_length=255, null=True, blank=True)    

    patch_version = models.CharField(
        max_length=11,
        verbose_name="Patch Version",
        null=True, blank=True)

    wiki_url = models.URLField(
        max_length=2000,
        verbose_name="Wiki Page",
        null=True, blank=True)
        

    def __str__(self):
        return f"[{self.owner.name}] {self.name}"


    def save(self, *args, **kwargs):
        super(Power, self).save(*args, **kwargs)

        if self.primary_overlay:
            image = Image.open(self.primary_overlay)
            width, height = image.size
            if (width != 256) or (height != 256):
                image = image.resize((256, 256), Image.ANTIALIAS)
                image.save(self.primary_overlay.path)           

        if self.secondary_overlay:
            image = Image.open(self.secondary_overlay)
            width, height = image.size
            if (width != 256) or (height != 256):
                image = image.resize((256, 256), Image.ANTIALIAS)
                image.save(self.secondary_overlay.path)     

        if self.tertiary_overlay:
            image = Image.open(self.tertiary_overlay)
            width, height = image.size
            if (width != 256) or (height != 256):
                image = image.resize((256, 256), Image.ANTIALIAS)
                image.save(self.tertiary_overlay.path)      