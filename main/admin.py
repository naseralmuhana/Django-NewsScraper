from __future__ import unicode_literals

from django.contrib import admin
from main import models as main_models


class NewsWebsiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url_', 'scraper', 'slug')
    list_display_links = ('name',)
    list_filter = ('name',)

    def url_(self, instance):
        return '<a href="{url}" target="_blank">{title}</a>'.format(
            url=instance.url, title=instance.url)

    url_.allow_tags = True


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'news_website_', 'url_', 'slug')
    list_display_links = ('title',)
    raw_id_fields = ('checker_runtime',)
    list_filter = ('news_website__name', 'create_at',)
    readonly_fields = ['create_at', 'update_at']

    def url_(self, instance):
        return '<a href="{url}" target="_blank">{title}</a>'.format(
            url=instance.url, title=instance.url)

    def news_website_(self, instance):
        return '<a href="{url}" target="_blank">{title}</a>'.format(
            url=instance.news_website.url, title=instance.news_website.name)

    url_.allow_tags = True
    news_website_.allow_tags = True


admin.site.register(main_models.NewsWebsite, NewsWebsiteAdmin)
admin.site.register(main_models.News, NewsAdmin)
admin.site.register(main_models.WebsiteInfo)
