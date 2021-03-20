from django.db import models

from PIL import Image

from game.storage import OverwriteStorage

def power_addon_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"addons/powers/{filename}"    

def item_addon_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"addons/items/{filename}"

def overlay_power_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"overlays/addons/powers/{filename}"
    
def overlay_item_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"overlays/addons/items/{filename}"        

class PowerAddOn(models.Model):

    class Meta:
        verbose_name = "Power Add-On"
        verbose_name_plural = "Power Add-Ons"   

    name = models.CharField(max_length=255, unique=True)
    power = models.ForeignKey(
        "game.Power", 
        on_delete=models.CASCADE)
    rarities = models.ManyToManyField(
        "game.Rarity",
        verbose_name="Rarities",
        blank=True,
    )

    description = models.TextField(null=True, blank=True)
    effects = models.ManyToManyField(
        "game.Effect", 
        verbose_name="Effects",
        blank=True)

    overlay = models.ImageField(
        upload_to=overlay_power_directory_path,
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
        return f"[{self.power.name}] {self.name}"


    def save(self, *args, **kwargs):
        super(PowerAddOn, self).save(*args, **kwargs)      

        if self.overlay:
            image = Image.open(self.overlay)
            width, height = image.size
            if (width != 256) or (height != 256):
                image = image.resize((256, 256), Image.ANTIALIAS)
                image.save(self.overlay.path)               

class ItemAddOn(models.Model):

    class Meta:
        verbose_name = "Item Add-On"
        verbose_name_plural = "Item Add-Ons"

    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(
        "game.ItemType", 
        on_delete=models.CASCADE)
    rarities = models.ManyToManyField(
        "game.Rarity",
        verbose_name="Rarities",
        blank=True,
    )
    description = models.TextField(null=True, blank=True)
    effects = models.ManyToManyField(
        "game.Effect", 
        verbose_name="Effects",
        blank=True)

    overlay = models.ImageField(
        upload_to=overlay_item_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )


    def __str__(self):
        return f"[{self.type}] {self.name}"


    def save(self, *args, **kwargs):
        super(ItemAddOn, self).save(*args, **kwargs)      

        if self.overlay:
            image = Image.open(self.overlay)
            width, height = image.size
            if (width != 256) or (height != 256):
                image = image.resize((256, 256), Image.ANTIALIAS)
                image.save(self.overlay.path)                  