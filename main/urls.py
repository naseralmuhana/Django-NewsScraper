from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from main import views as main_views

app_name = 'main'

urlpatterns = [

    url(r'^$', main_views.HomePageView.as_view(), name="home"),

    url(r'^search', main_views.SearchForm.as_view(), name="search_news"),
    url(r'^(?P<slug>[\w-]+)/$', main_views.news_list, name="news_list"),
    url(r'^(?P<username>[\w-]+)/watch-later-list/', main_views.watch_later_list, name="watch_later_list"),
    url(r'^(?P<username>[\w-]+)/history/', main_views.history_list, name="history"),

    url(r'^(?P<website_slug>[\w-]+)/(?P<slug>[\w-]+)/$', main_views.NewsDetailsView.as_view(), name="news_detail"),
    url(r'hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),

    url(r'^watch-later/(?P<id>\d+)', main_views.watch_later_add_remove, name="watch_later_add_remove"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    