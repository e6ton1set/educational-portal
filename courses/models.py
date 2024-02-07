from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField


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
                              on_delete=models.CASCADE,
                              verbose_name='Тренер')
    program = models.ForeignKey(Program,
                                related_name='courses',
                                on_delete=models.CASCADE,
                                verbose_name='Программа')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Заголовок латиницей')
    review = models.TextField(verbose_name='Краткое описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Курс {self.title}"


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE,)
    title = models.CharField(max_length=128, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.title}"


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE,
                               verbose_name='Модуль')

    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file')},
                                     verbose_name='Тип содержимого')
    object_id = models.PositiveIntegerField(verbose_name='ID объекта')
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True,
                       for_fields=['module'],
                       verbose_name='Порядок')

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    coach = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.title}"


class Text(ItemBase):
    content = models.TextField(verbose_name='Описание')


class File(ItemBase):
    file = models.FileField(upload_to='files', verbose_name='Файл')


class Image(ItemBase):
    file = models.FileField(upload_to='images', verbose_name='Изображение')


class Video(ItemBase):
    url = models.URLField(verbose_name='Видео')
