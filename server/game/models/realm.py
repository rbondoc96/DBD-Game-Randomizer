from django.db import models

from game.storage import OverwriteStorage

def realm_directory_path(instance, filename):
    filename = f"{instance.name}" + "." + filename.split(".").pop()
    return f"maps/{filename}"

class Realm(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        upload_to=realm_directory_path,
        storage=OverwriteStorage(),
        blank=True,
        null=True,
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
        return f"{self.name}"