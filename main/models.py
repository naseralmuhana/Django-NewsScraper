# built it
from django.db.models.signals import pre_delete, pre_save
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.dispatch import receiver
from django.db import models

# outside
from hitcount.models import HitCountMixin, HitCount
from scrapy_djangoitem import DjangoItem
from dynamic_scraper.models import Scraper, SchedulerRuntime
from datetime import datetime

# my own project
from NewsScraper.utils import unique_slug_generator_name, unique_slug_generator_title


class WebsiteInfo(models.Model):
    key = models.CharField(max_length=30)
    search_domain = models.CharField(max_length=200)
    scraper = models.ForeignKey(
        Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(
        max_length=256, upload_to='website_pics', blank=True, null=True)

    def __str__(self):
        return self.key


class NewsWebsite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(
        Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(
        SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_website_name(self):
        return self.name[:3]


class News(models.Model):
    title = models.CharField(max_length=200)
    news_website = models.ForeignKey(NewsWebsite)
    description = models.TextField(blank=True)
    image = models.URLField()
    url = models.URLField()
    watch_later = models.ManyToManyField(
        User, related_name='watch_later', blank=True)
    checker_runtime = models.ForeignKey(
        SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True, null=True, blank=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # def get_date(self):
    #     time = datetime.now()
    #     if self.create_at.day == time.day:
    #         return str(time.hour - self.create_at.hour) + " hours ago"
    #     else:
    #         if self.create_at.month == time.month:
    #             return str(time.day - self.create_at.day) + " days ago"
    #         else:
    #             if self.create_at.year == time.year:
    #                 return str(time.month - self.create_at.month) + " months ago"
    #     return self.create_at


class NewsItem(DjangoItem):
    django_model = News


@receiver(pre_delete)
def pre_delete_handler(sender, instance, using, **kwargs):
    if isinstance(instance, News):
        if instance.checker_runtime:
            instance.checker_runtime.delete()


pre_delete.connect(pre_delete_handler)


# function to create a slug using the function (unique_slug_generator_name) that exist in the module (utils.py)
def create_slug_name(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_name(instance)


# function to create a slug using the function (unique_slug_generator_title) that exist in the module (utils.py)
def create_slug_title(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_title(instance)


pre_save.connect(create_slug_name, sender=NewsWebsite)
pre_save.connect(create_slug_title, sender=News)
