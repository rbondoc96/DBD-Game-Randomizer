from django.db import models

from PIL import Image

from game.storage import OverwriteStorage

def power_addon_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"addons/powers/{filename}"    

def item_addon_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"addons/items/{filename}"

def template_power_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"templates/addons/powers/{filename}"
    
def template_item_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"templates/addons/items/{filename}"        

class PowerAddOn(models.Model):
    name = models.CharField(max_length=255, unique=True)
    power = models.ForeignKey(
        "game.Power", 
        on_delete=models.CASCADE)
    rarity = models.ForeignKey(
        "game.Rarity", 
        null=True, 
        on_delete=models.SET_NULL)
    description = models.TextField()
    effects = models.ManyToManyField("game.Effect", verbose_name="Effects")

    # Template overlay that will be put overlay the bg+border layer 
    # May or may not be transparent bg
    template = models.ImageField(
        upload_to=template_power_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )    

    # Converted image
    image = models.ImageField(
        upload_to=power_addon_directory_path, 
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )    

    def __str__(self):
        return f"[{self.power.name}] {self.name}"

    def save(self, *args, **kwargs):
        super(PowerAddOn, self).save(*args, **kwargs)
        
        if self.image:
            image = Image.open(self.image)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.image.path)   

        if self.template:
            image = Image.open(self.template)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.template.path)                 

    class Meta:
        verbose_name = "Power Add-On"
        verbose_name_plural = "Power Add-Ons"    

class ItemAddOn(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(
        "game.ItemType", 
        on_delete=models.CASCADE)
    rarity = models.ForeignKey(
        "game.Rarity", 
        null=True, 
        on_delete=models.SET_NULL)
    description = models.TextField()
    effects = models.ManyToManyField("game.Effect", verbose_name="Effects")

    # Template overlay that will be put overlay the bg+border layer 
    # May or may not be transparent bg
    template = models.ImageField(
        upload_to=template_item_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )

    # Converted image
    image = models.ImageField(
        upload_to=item_addon_directory_path, 
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )    

    def __str__(self):
        return f"[{self.type}] {self.name}"

    def save(self, *args, **kwargs):
        super(ItemAddOn, self).save(*args, **kwargs)
        
        if self.image:
            image = Image.open(self.image)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.image.path)  

        if self.template:
            image = Image.open(self.template)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.template.path)                  

    class Meta:
        verbose_name = "Item Add-On"
        verbose_name_plural = "Item Add-Ons"