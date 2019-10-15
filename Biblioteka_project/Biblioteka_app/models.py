from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import URLValidator


class Book(models.Model):
    title = models.TextField(null=True)
    authors = ArrayField(ArrayField(models.TextField(null=True)))
    published_date = models.DateField(null=True)
    page_count = models.IntegerField(null=True)
    image_links = models.ForeignKey('ImageLinks', on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=10, null=True)


class IndustryIdentifiers(models.Model):
    type = models.TextField(null=True)
    identifier = models.TextField(null=True)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)


class ImageLinks(models.Model):
    small_thumbnail = models.TextField(validators=[URLValidator()], null=True)
    thumbnail = models.TextField(validators=[URLValidator()], null=True)
    small = models.TextField(validators=[URLValidator()], null=True)
    medium = models.TextField(validators=[URLValidator()], null=True)
    large = models.TextField(validators=[URLValidator()], null=True)
    extra_large = models.TextField(validators=[URLValidator()], null=True)