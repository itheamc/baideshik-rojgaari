from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_jobs, name="Home"),
    path('jobs_country_wise', views.jobs_country_wise, name="jobs_country_wise"),
    # path('delete', views.jobs_delete, name="update"),
]