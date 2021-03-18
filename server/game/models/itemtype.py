from django.db import models

class ItemType(models.Model):
    
    class Meta:
        verbose_name = "Item Type"
        verbose_name_plural = "Item Types"    

    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type