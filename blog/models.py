from django.db import models


# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name='заголовок')
    slug = models.CharField(max_length=250, verbose_name='slug', blank=True, null=True)
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='превью', blank=True, null=True)
    date_create = models.DateTimeField(verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    view_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
