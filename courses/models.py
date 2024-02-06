from django.db import models
from django.contrib.auth.models import User


class Program(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"Программа {self.title}"


class Course(models.Model):
    coach = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    program = models.ForeignKey(Program,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Курс {self.title}"


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"Модуль {self.title}"