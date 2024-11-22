from django.contrib.auth.models import User  # type: ignore
from django.db import models  # type: ignore


class Room(models.Model):
    name = models.CharField(max_length=65, unique=True)
    description = models.CharField(max_length=254)
    notes = models.CharField(max_length=65, blank=True, null=True)
    responsible = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.name}"


class Component(models.Model):
    inventory_number = models.CharField(max_length=65, blank=True)
    description = models.CharField(max_length=254)
    brand = models.CharField(max_length=65, blank=True)
    model = models.CharField(max_length=65, blank=True)
    condition = models.CharField(max_length=65, blank=True)
    notes = models.CharField(max_length=65, blank=True, null=True)
    location = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
    location_name = models.CharField(max_length=65, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.description}"

    def save(self, *args, **kwargs):
        if self.location:
            self.location_name = self.location.name
        else:
            self.location_name = None

        return super(Component, self).save(*args, **kwargs)
