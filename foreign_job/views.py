from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .models import ForeignJob, Country, Company, JobSkillOrTitle
from app_user.models import AppUser
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes, authentication_classes

UserModel = get_user_model()


# def jobs_delete(request):
#     jobs = ForeignJob.objects.all()
#     for job in jobs:
#         job.delete()
#
#     skills = JobSkillOrTitle.objects.all()
#     for skill in skills:
#         skill.delete()
#
#     companies = Company.objects.all()
#     for company in companies:
#         company.delete()
#     return JsonResponse({'success': True})

# Update Country
# def update_company(request):
#     jobs = ForeignJob.objects.all()
#     companies = []
#     for job in jobs:
#         company = Company.objects.filter(name__iexact=job.company_name)
#         if company.exists():
#             continue
#         new_company = Company.objects.create(name=job.company_name)
#         companies.append(new_company.as_dict)
#
#     return JsonResponse({'status': 'success', 'companies': companies}, safe=False)


# def update_company(request):
#     jobs = ForeignJob.objects.all()
#     for job in jobs:
#         company = Company.objects.filter(name__iexact=job.company_name)
#         if company.exists():
#             job.company = company.first()
#             job.save()
#
#     return JsonResponse({'status': 'success'}, safe=False)

# Views to return the list of jobs to the ap user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_jobs(request):
    try:

        # Extracting user from the request
        user = request.user

        # Getting the app user based on auth user
        app_user = AppUser.objects.get(user=user)

        # Suggested Jobs
        # As per the recent views
        suggested_jobs_queryset = app_user.jobs_as_per_recent_views()
        suggested_jobs = [job.as_dict for job in suggested_jobs_queryset] if suggested_jobs_queryset else []

        # Often Searched Jobs
        # As per the recent searches
        often_searched_jobs_queryset = app_user.jobs_as_per_recent_searches(limit=50)
        often_searched_jobs = often_searched_jobs_queryset.difference(
            suggested_jobs_queryset) if often_searched_jobs_queryset and suggested_jobs_queryset else often_searched_jobs_queryset if often_searched_jobs_queryset else []
        often_searched_jobs = [job.as_dict for job in often_searched_jobs[:20]]

        # Your recently viewed jobs
        recently_viewed_jobs = [job.job.as_dict for job in app_user.user_viewed_jobs[:20]]

        # Recently added jobs
        is_new_user = len(suggested_jobs) == 0 and len(often_searched_jobs) == 0 and len(recently_viewed_jobs) == 0
        recently_added_jobs_queryset = ForeignJob.apply_filters(
            filters={'deadline__icontains': 'days', 'for_female': app_user.gender == 'female'},
            limit=20 if not is_new_user else 200,
            offset=0)
        recently_added_jobs = [job.as_dict for job in recently_added_jobs_queryset]

        # Creating the response dict
        response = [
            {
                'label': 'Recently Added Jobs',
                'total_jobs': len(recently_added_jobs),
                'jobs': recently_added_jobs
            },
            {
                'label': 'Suggested Jobs',
                'total_jobs': len(suggested_jobs),
                'jobs': suggested_jobs
            },
            {
                'label': 'Jobs you often search for',
                'total_jobs': len(often_searched_jobs),
                'jobs': often_searched_jobs
            },
            {
                'label': 'Recently Viewed',
                'total_jobs': len(recently_viewed_jobs),
                'jobs': recently_viewed_jobs
            },
        ]

        # Formatting the response
        formatted_responses = {
            'status': 'success',
            'message': 'Jobs fetched successfully',
            'data': {
                'has_sections': not is_new_user,
                'jobs': recently_added_jobs if is_new_user else [j for j in response if j['total_jobs'] > 0]
            }
        }

        # Returning the response
        return Response(formatted_responses, status=status.HTTP_200_OK)

    except Exception as e:
        error_responses = {
            'status': 'error',
            'message': e.__str__(),
        }
        return Response(error_responses, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def jobs_country_wise(request):
    filters = {
        'deadline__icontains': 'days',
        # 'country__name__icontains': 'Qatar',
        'for_female': True,
        # 'skill_or_title__title__icontains': "house"
    }
    jobs = ForeignJob.objects.filter(**filters).order_by('-deadline')

    # categories jobs as country
    response = []
    countries = Country.objects.all()

    for country in countries:
        response.append(
            {'id': country.id, 'country': country.name,
             'jobs': [job.as_dict_without_country for job in jobs if job.country.name == country.name]})

    final_response = [res for res in response if len(res['jobs']) > 0]

    return Response(final_response)
