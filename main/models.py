from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
    
class City(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True)
    
    def __str__(self):
        return self.name
    
class Activity(models.Model):
    name = models.CharField()
    description = models.CharField()
    price = models.FloatField()
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        null=True,
        to_field='name'
    )
    duration = models.TimeField(null=True)
    has_badge_excellence = models.BooleanField(null=True)
    recommendation_rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True
    )

    def __str__(self):
        return f"{self.name} ; {self.description} ; {self.price} ; {self.city} ; {self.duration} ; {self.has_badge_excellence } ; {self.recommendation_rate}"
    

    
    
