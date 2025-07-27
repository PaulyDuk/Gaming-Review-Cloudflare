from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    founded_year = models.IntegerField(blank=True, null=True)
    headquarters = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    logo = CloudinaryField('image', default='placeholder')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name