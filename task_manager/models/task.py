from django.db import models
from .category import Category

class Task(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('PENDING', 'Pending'),
        ('BLOCKED', 'Blocked'),
        ('DONE', 'Done'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Я так понимаю "title: Название задачи. Уникально для даты." имеется ввиду уникально для дедлайна?
    class Meta:
        unique_together = ('title', 'deadline')
        ordering = ['-created_at'] #order by

    def __str__(self):
        return self.title
