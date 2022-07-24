from django.shortcuts import render
from django.http import JsonResponse
from .models import ForeignJob


# Create your views here.

def index(request):
    filters = {
        'deadline__icontains': 'days',
        # 'country_name__icontains': 'Qatar',
        'for_female': False
    }
    jobs = ForeignJob.objects.filter(**filters).order_by('-deadline')
    res = [job.as_dict for job in jobs]
    return JsonResponse(res, safe=False)


def jobs_country_wise(request):
    filters = {
        'deadline__icontains': 'days',
        # 'country_name__icontains': 'Qatar',
        'for_female': True,
        'skill_name__icontains': "house"
    }
    jobs = ForeignJob.objects.filter(**filters).order_by('-deadline')

    print(jobs.exists())
    # categories jobs as country
    response = []
    countries = set()

    for job in jobs:
        countries.add(job.country_name)

    for country in countries:
        response.append({'country': country, 'jobs': [job.as_dict for job in jobs if job.country_name == country]})

    return JsonResponse(response, safe=False)
