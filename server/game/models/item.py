from django.db import models

from game.models import Rarity, Effect

class ItemType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Item Type"
        verbose_name_plural = "Item Types"

class Item(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    rarity = models.ForeignKey(Rarity, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    effects = models.ManyToManyField(Effect, verbose_name="Effects")
    quote = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"[{self.type}] {self.name}"
    
    class Meta:
        ordering = ["type"]
