# built it
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q

# outside
from hitcount.views import HitCountDetailView
from hitcount import models as hitcount_models

# my own project
from main import models as main_models
from main.tasks import single_crawl_without_scheduling
from main.weather import get_weather


class HomePageView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        context['most_popular'] = main_models.News.objects.order_by('-hit_count_generic__hits')[:3]
        context['most_popular_ny_times'] = main_models.News.objects.filter(
            news_website__name__startswith='New York Times').order_by('-hit_count_generic__hits')[:5]
        context['most_popular_roya'] = main_models.News.objects.filter(
            news_website__name__startswith='Roya').order_by('-hit_count_generic__hits')[:5]
        context['most_popular_jordan_times'] = main_models.News.objects.filter(
            news_website__name__startswith='Jordan Times').order_by('-hit_count_generic__hits')[:5]
        context['most_popular_aljazeera'] = main_models.News.objects.filter(
            news_website__name__startswith='Aljazeera').order_by('-hit_count_generic__hits')[:5]
        context['most_popular_technology'] = main_models.News.objects.filter(
            news_website__name__startswith='Technology').order_by('-hit_count_generic__hits')[:5]
        context['most_popular_business'] = main_models.News.objects.filter(
            news_website__name__startswith='Business').order_by('-hit_count_generic__hits')[:5]
        return context


def news_list(request, slug):

    news_list = main_models.News.objects.filter(
        news_website__slug=slug).order_by('-create_at', 'title')
    context = {
        'news_list': pagination(request, news_list),
    }
    context.update(strip_website_name_and_breadcrumb(slug))
    return render(request, 'main/news_list.html', context)


class NewsDetailsView(HitCountDetailView):
    model = main_models.News
    template_name = 'main/news_detail.html'
    context_object_name = 'news_detail'
    slug_field = 'slug'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(NewsDetailsView, self).get_context_data(**kwargs)
        news_title = main_models.News.objects.get(slug=self.kwargs['slug'])

        context['website_slug'] = self.kwargs['website_slug']
        context['most_popular_news'] = main_models.News.objects.filter(
            Q(news_website__slug=self.kwargs['website_slug']) &
            ~Q(title=news_title.title)
        ).order_by('-hit_count_generic__hits')[:8]

        context.update(strip_website_name_and_breadcrumb(
            self.kwargs['website_slug']))
        return context


class SearchForm(TemplateView):

    def get(self, request, *args, **kwargs):
        text = str(request.GET['search_text']).strip(' !@#$%^&*()_+-')
        websites_list = request.GET.getlist('check')
        context = {'search_result': 'exits', }

        if text:
            context['text'] = text
            text_split = text.split(' ')
            text_split = ('_'.join(text_split)).strip('_')
            data_news = []
            news_count = 0
            if websites_list:
                for website in websites_list:
                    result = main_models.News.objects.filter(
                        (Q(title__icontains=text) &
                         Q(news_website__name__startswith=website))
                        |
                        (Q(news_website__name__icontains=text_split) &
                         Q(news_website__name__startswith=website))
                    ).order_by('-create_at')
                    data_news += result
                    news_count += result.count()

                if data_news == []:
                    there_have_news = single_crawl_without_scheduling(
                        text, websites_list)
                    for website in websites_list:
                        result = main_models.News.objects.filter(
                            (Q(title__icontains=text) &
                             Q(news_website__name__startswith=website))
                            |
                            (Q(news_website__name__icontains=text_split) &
                             Q(news_website__name__startswith=website))
                        ).order_by('-create_at')
                        data_news += result
                        news_count += result.count()

                context['news_count'] = news_count
                context['news_list'] = pagination(request, data_news)
                context['websites_list'] = websites_list
                context['websites_list_search'] = websites_list
                return render(request, 'main/news_list.html', context)

            else:
                data_news = main_models.News.objects.filter(
                    Q(title__icontains=text) |
                    Q(news_website__name__icontains=text_split)
                ).order_by('-create_at')
                context['news_count'] = data_news.count
                context['news_list'] = pagination(request, data_news)
                return render(request, 'main/news_list.html', context)

        else:
            messages.error(request, "Invalid Text, please try again!")
            return redirect(reverse('main:home'))


@ login_required(login_url='/account/register-login')
def watch_later_add_remove(request, id):
    url = request.META.get('HTTP_REFERER')
    news = get_object_or_404(main_models.News, id=id)
    if news.watch_later.filter(id=request.user.id).exists():
        news.watch_later.remove(request.user)
        # messages.warning(request, f'{book.name} removed from favourites.')
    else:
        news.watch_later.add(request.user)
        # messages.success(request, f'{book.name} added to favourites.')
    if 'account' in url:
        return HttpResponseRedirect("/")
    return HttpResponseRedirect(url)


@ login_required(login_url='/account/register-login')
def watch_later_list(request, username):

    watch_later_news = main_models.News.objects.filter(
        watch_later=request.user.id)

    news_count = watch_later_news.count
    context = {
        'watch_later': 'exist',
        'news_count': news_count,
        'news_list': pagination(request, watch_later_news)
    }
    return render(request, 'main/news_list.html', context)


@ login_required(login_url='/account/register-login')
def history_list(request, username):

    history_list = hitcount_models.Hit.objects.filter(user_id=request.user.id)
    data_news = []
    news_count = 0
    if history_list:
        for news in history_list:
            result = main_models.News.objects.filter(
                title__icontains=news.hitcount)
            data_news += result
            news_count += result.count()

    context = {
        'history': 'exist',
        'news_count': news_count,
        'history_list': history_list,
        'news_list': pagination(request, data_news)
    }

    return render(request, 'main/news_list.html', context)


def strip_website_name_and_breadcrumb(slug):

    context = {}
    website_breadcrumb = ''
    websites_names = ''

    names = ['Technology', 'Business', 'New York Times ',
             'Roya ', 'Jordan Times', 'Aljazeera ']

    website_breadcrumb = main_models.NewsWebsite.objects.filter(
        slug=slug)[0]
    websites_names = str(website_breadcrumb.name)
    for name in names:
        if name in websites_names:
            context['website_categories'] = main_models.NewsWebsite.objects.filter(
                name__startswith=name)
            break
    context['website_breadcrumb'] = website_breadcrumb
    return context


# function to check if the slug is exist and return none if not.
def check_on_slug(slug):

    if slug.exists():
        slug = slug.first()
        return slug
    else:
        return None


def pagination(request, news_list):

    paginator = Paginator(news_list, 9)
    page = request.GET.get('page', 1)
    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        news_list = paginator.page(1)
    except EmptyPage:
        news_list = paginator.page(paginator.num_pages)

    return news_list
