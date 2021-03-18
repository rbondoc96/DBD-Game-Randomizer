from django.db import models

class Rarity(models.Model):
    
    class Meta:
        verbose_name_plural = "Rarities"    
    
    rarity = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.rarity