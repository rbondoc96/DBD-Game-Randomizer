from django.db import models

class ItemType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Item Type"
        verbose_name_plural = "Item Types"