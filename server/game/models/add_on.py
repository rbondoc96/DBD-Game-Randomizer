from django.db import models

from game.models import Rarity, Effect, ItemType

class AddOn(models.Model):
    name = models.CharField(max_length=255)
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    rarity = models.ForeignKey(Rarity, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    effects = models.ManyToManyField(Effect, verbose_name="Effects")

    def __str__(self):
        return f"[{self.item_type}] {self.name}"

    class Meta:
        verbose_name_plural = "Add-Ons"