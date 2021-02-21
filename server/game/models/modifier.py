from django.db import models

class ModifierType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Modifier Type"

class ModifierUnit(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Modifier Unit"

class Modifier(models.Model):
    type = models.ForeignKey(
        ModifierType, 
        on_delete=models.SET_NULL, 
        null=True
    )
    description = models.CharField(max_length=255)
    unit = models.ForeignKey(
        ModifierUnit, 
        on_delete=models.SET_NULL, 
        null=True
    )
    value = models.IntegerField()

    def __str__(self):
        return f"{self.description}"