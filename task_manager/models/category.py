from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories' #в админке было Categorys
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name'),
        ]

