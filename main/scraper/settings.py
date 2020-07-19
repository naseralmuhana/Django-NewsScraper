from __future__ import unicode_literals
# Scrapy settings for crawling project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import os, sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsScraper.settings")
# sys.path.insert(0, os.path.join(PROJECT_ROOT, "../..")) #only for example_project

BOT_NAME = 'main'

# Setting LOG_STDOUT to True will prevent Celery scheduling to work, 2017-06-06
# If you know the cause or a fix please report on GitHub
LOG_STDOUT = False
LOG_LEVEL = 'INFO'

SPIDER_MODULES = ['dynamic_scraper.spiders', 'main.scraper', 'main.scraper.checkers', ]
USER_AGENT = '{b}/{v}'.format(b=BOT_NAME, v='1.0')

ITEM_PIPELINES = {
    'dynamic_scraper.pipelines.ValidationPipeline': 400,
    'main.scraper.pipelines.DjangoWriterPipeline': 800,
}


DSCRAPER_LOG_ENABLED = True
DSCRAPER_LOG_LEVEL = 'ERROR'
DSCRAPER_LOG_LIMIT = 5
DSCRAPER_SPLASH_ARGS = { 'wait': 1000 }
