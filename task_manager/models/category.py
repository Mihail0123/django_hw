from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories' #в админке было Categorys

    def __str__(self):
        return self.name