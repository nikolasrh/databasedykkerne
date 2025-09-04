from django.db import models

# Create your models here.

class Car(models.Model):
    brand = models.CharField(max_length=20)
    year = models.IntegerField()

    def __str__(self):
        return self.brand + " " + self.year

class User(models.Model):
    name = models.CharField(max_length=100)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="owners", default=5)

    def __str__(self):
        return self.name