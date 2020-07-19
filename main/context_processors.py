from main import models as main_models
from main.weather import get_weather


def herder_content():

    context = {}

    context['ny_middle_east_header'] = main_models.News.objects.filter(
        news_website__name='New York Times Middle East').order_by('-create_at')[:8]
    context['ny_europe_header'] = main_models.News.objects.filter(
        news_website__name='New York Times Europe').order_by('-create_at')[:8]
    context['ny_americas_header'] = main_models.News.objects.filter(
        news_website__name='New York Times Americas').order_by('-create_at')[:8]
    context['ny_asia_header'] = main_models.News.objects.filter(
        news_website__name='New York Times Asia').order_by('-create_at')[:8]

    context['roya_jordan_header'] = main_models.News.objects.filter(
        news_website__name='Roya Jordan').order_by('-create_at')[:8]
    context['roya_palestine_header'] = main_models.News.objects.filter(
        news_website__name='Roya Palestine').order_by('-create_at')[:8]
    context['roya_world_header'] = main_models.News.objects.filter(
        news_website__name='Roya World').order_by('-create_at')[:8]

    context['jordan_times_local_header'] = main_models.News.objects.filter(
        news_website__name='Jordan Times Local').order_by('-create_at')[:8]
    context['jordan_times_region_header'] = main_models.News.objects.filter(
        news_website__name='Jordan Times Region').order_by('-create_at')[:8]
    context['jordan_times_world_header'] = main_models.News.objects.filter(
        news_website__name='Jordan Times World').order_by('-create_at')[:8]

    context['aljazeera_middle_east_header'] = main_models.News.objects.filter(
        news_website__name='Aljazeera Middle East').order_by('-create_at')[:8]
    context['aljazeera_europe_header'] = main_models.News.objects.filter(
        news_website__name='Aljazeera Europe').order_by('-create_at')[:8]
    context['aljazeera_us_canada_header'] = main_models.News.objects.filter(
        news_website__name='Aljazeera US & Canada').order_by('-create_at')[:8]
    context['aljazeera_asia_header'] = main_models.News.objects.filter(
        news_website__name='Aljazeera Asia').order_by('-create_at')[:8]

    context['tech_ny_times_header'] = main_models.News.objects.filter(
        news_website__name='Technology New York Times').order_by('-create_at')[:8]
    context['tech_aljazeera_header'] = main_models.News.objects.filter(
        news_website__name='Technology Aljazeera').order_by('-create_at')[:8]
    context['tech_verge_header'] = main_models.News.objects.filter(
        news_website__name='Technology Verge').order_by('-create_at')[:8]

    context['business_arabian_business_header'] = main_models.News.objects.filter(
        news_website__name='Business Arabian Business').order_by('-create_at')[:8]
    context['business_bbc_header'] = main_models.News.objects.filter(
        news_website__name='Business BBC').order_by('-create_at')[:8]
    context['business_ny_times_header'] = main_models.News.objects.filter(
        news_website__name='Business New York Times').order_by('-create_at')[:8]

    # for main menu for mobile
    context['new_york_times_mobile'] = main_models.NewsWebsite.objects.filter(
        name__startswith='New York Times')
    context['roya_mobile'] = main_models.NewsWebsite.objects.filter(
        name__startswith='Roya')
    context['jordan_times_mobile'] = main_models.NewsWebsite.objects.filter(
        name__startswith='Jordan Times')
    context['aljazeera_mobile'] = main_models.NewsWebsite.objects.filter(
        name__startswith='Aljazeera')
    context['technology_mobile'] = main_models.NewsWebsite.objects.filter(
        name__startswith='Technology')
    context['business_mobile'] = main_models.NewsWebsite.objects.filter(
        name__startswith='Business')

    # trending now below the navbar
    context['trending_now'] = main_models.News.objects.all().order_by(
        '-create_at')[:20]

    # website slug
    context['ny_website_name'] = main_models.NewsWebsite.objects.filter(
        name__startswith='New York Times')
    context['roya_website_name'] = main_models.NewsWebsite.objects.filter(
        name__startswith='Roya Jordan')
    context['jordan_times_website_name'] = main_models.NewsWebsite.objects.filter(
        name__startswith='Jordan Times Local')
    context['aljazeera__website_name'] = main_models.NewsWebsite.objects.filter(
        name__startswith='Aljazeera Middle East')
    context['tech__website_name'] = main_models.NewsWebsite.objects.filter(
        name__startswith='Technology New York Times')
    context['business__website_name'] = main_models.NewsWebsite.objects.filter(
        name__startswith='Business Arabian Business')

    return context


def get_websites(request):
    websites = main_models.WebsiteInfo.objects.all()
    context = {
        'websites': websites,
    }
    context.update(get_weather())
    context.update(herder_content())
    return context
