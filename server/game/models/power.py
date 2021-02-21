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

def primary_template_directory_path(instance, filename):
    filename = f"{instance.name}-primary" + "." + filename.split(".").pop()
    return f"templates/powers/{filename}"    

def secondary_template_directory_path(instance, filename):
    filename = f"{instance.name}-secondary" + "." + filename.split(".").pop()
    return f"templates/powers/{filename}"     

def tertiary_template_directory_path(instance, filename):
    filename = f"{instance.name}-tertiary" + "." + filename.split(".").pop()
    return f"templates/powers/{filename}"    

class Power(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.OneToOneField(
        "game.Character",
        on_delete=models.CASCADE, 
        primary_key=False
    )
    description = models.TextField()
    effects = models.ManyToManyField("game.Effect", verbose_name="Effects")

    # Template overlay that will be put overlay the bg+border layer 
    # May or may not be transparent bg
    primary_template = models.ImageField(
        upload_to=primary_template_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )
    secondary_template = models.ImageField(
        upload_to=secondary_template_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )
    tertiary_template = models.ImageField(
        upload_to=tertiary_template_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )

    # Composed image
    primary_image = models.ImageField(
        upload_to=primary_power_directory_path, 
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )
    secondary_image = models.ImageField(
        upload_to=secondary_power_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )
    tertiary_image = models.ImageField(
        upload_to=tertiary_power_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True
    )    
    quote = models.CharField(max_length=255, null=True, blank=True)    

    def __str__(self):
        return f"[{self.owner.name}] {self.name}"

    def save(self, *args, **kwargs):
        super(Power, self).save(*args, **kwargs)
        
        if self.primary_image:
            image = Image.open(self.primary_image)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.primary_image.path)  
        
        if self.secondary_image:
            image = Image.open(self.secondary_image)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.secondary_image.path) 

        if self.primary_template:
            image = Image.open(self.primary_template)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.primary_template.path)   

        if self.secondary_template:
            image = Image.open(self.secondary_template)
            image = image.resize((256, 256), Image.ANTIALIAS)
            image.save(self.secondary_template.path)                   
    
    class Meta:
        ordering = ["owner"]
        

        
