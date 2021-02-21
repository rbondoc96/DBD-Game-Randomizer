from django.db import models

class EffectType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Effect Type"
        verbose_name_plural = "Effect Types"

class Effect(models.Model):
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

    class Meta:
        ordering = ["type"]