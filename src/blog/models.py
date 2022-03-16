from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import format_html
from extensions.utils import jalali_converter


# My Managers
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, default=None, blank=True
                               , verbose_name='زیر دسته', on_delete=models.SET_NULL, related_name='children')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='فعال')
    position = models.IntegerField(verbose_name='پوزیشن')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['position']

    def __str__(self):
        return self.title
    objects = CategoryManager()


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده')
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles', verbose_name='نویسنده')
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس مقاله')
    category = models.ManyToManyField(Category, verbose_name='دسته بندی', related_name='articles')
    description = models.TextField(verbose_name='محتوا')
    thumbnail = models.ImageField(upload_to="images", verbose_name='تصویر مقاله')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = "زمان انتشار"

    def thumbnail_tag(self):
        return format_html("<img width=100 height= 75 style='border-radius: 5px;vertical-align: center;' src='{}'>".format(self.thumbnail.url))

    thumbnail_tag.short_description = "تصویر"
    objects = ArticleManager()
