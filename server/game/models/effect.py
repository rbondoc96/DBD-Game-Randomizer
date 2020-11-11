from django.db import models

# class Buff(models.Model):
#     summary = models.CharField()
#     pass

# class Debuff(models.Model):
#     summary = models.CharField()
#     pass

# class SpecialAction(models.Model):
#     summary = models.CharField()
#     pass

# class SpecialEffect(models.Model):
#     summary = models.CharField()
#     pass

class EffectType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Effect Type"
        verbose_name_plural = "Effect Types"

class Effect(models.Model):
    summary = models.CharField(max_length=255)
    type = models.ForeignKey(EffectType, null=True, on_delete=models.SET_NULL)

    affects_all = models.BooleanField(
        default=False,
        verbose_name="Does the Effect affect ALL players?")

    def __str__(self):
        return f"[{self.type}] {self.summary}"

    class Meta:
        ordering = ["type"]