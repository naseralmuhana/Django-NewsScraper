# from dynamic_scraper.spiders.django_checker import DjangoChecker
# from main import models as main_models


# class ArticleChecker(DjangoChecker):
#     name = 'news_checker'

#     def __init__(self, *args, **kwargs):
#         self._set_ref_object(main_models.News, **kwargs)
#         self.scraper = self.ref_object.news_website.scraper
#         self.scheduler_runtime = self.ref_object.checker_runtime
#         super(ArticleChecker, self).__init__(self, *args, **kwargs)
