from django.db import models

class EffectType(models.Model):
    
    class Meta:
        verbose_name = "Effect Type"
        verbose_name_plural = "Effect Types"
    
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

class Effect(models.Model):
    
    class Meta:
        ordering = ["type"]
    
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.ForeignKey(EffectType, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=255, unique=True)

    modifiers = models.ManyToManyField("game.Modifier", blank=True)
    conditions = models.ManyToManyField("game.Condition", blank=True)

    affects_all = models.BooleanField(
        default=False,
        verbose_name="Does the Effect affect ALL players?")

    def __str__(self):
        return f"[{self.type}] {self.description}"