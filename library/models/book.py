from django.db import models


class Book(models.Model):
    title = models.CharField(
        max_length=65
    )
    description = models.TextField()
    published_date = models.DateField()

    def __str__(self):
        return self.title