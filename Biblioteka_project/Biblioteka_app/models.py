from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import URLValidator


class Book(models.Model):
    title = models.TextField()
    author = ArrayField(ArrayField(models.TextField()))
    published_date = models.DateField()
    page_count = models.IntegerField()
    image_links = models.ForeignKey('ImageLinks',on_delete=models.CASCADE)
    language = models.CharField(max_length=10)


class IndustryIdentifiers(models.Model):
    type = models.TextField()
    identifier = models.TextField(unique=True)
    book = models.ForeignKey('Book',on_delete=models.CASCADE)


class ImageLinks(models.Model):
    small_thumbnail = models.TextField(validators=[URLValidator()],blank=True)
    thumbnail = models.TextField(validators=[URLValidator()],blank=True)
    small = models.TextField(validators=[URLValidator()],blank=True)
    medium = models.TextField(validators=[URLValidator()],blank=True)
    large = models.TextField(validators=[URLValidator()],blank=True)
    extraLarge = models.TextField(validators=[URLValidator()],blank=True)
