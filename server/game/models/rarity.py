from django.db import models

class Rarity(models.Model):
    rarity = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.rarity

    class Meta:
        verbose_name_plural = "Rarities"