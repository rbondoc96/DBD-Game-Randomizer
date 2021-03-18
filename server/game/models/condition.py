from django.db import models

class ConditionType(models.Model):
    
    class Meta:
        verbose_name = "Condition Type"
    
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class Condition(models.Model):
    event = models.ForeignKey("game.Event", on_delete=models.CASCADE)
    type = models.ForeignKey(ConditionType, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)    

    def __str__(self):
        return f"{self.description}"