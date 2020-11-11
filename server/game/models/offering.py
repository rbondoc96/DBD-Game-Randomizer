from django.db import models

from game.models import Rarity, Effect

class Offering(models.Model):
    name = models.CharField(unique=True, max_length=255)
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    description = models.TextField()
    effects = models.ManyToManyField(Effect, verbose_name="Effects")
    quote = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name