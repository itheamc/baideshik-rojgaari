from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Home"),
    path('jobs_country_wise', views.jobs_country_wise, name="jobs_country_wise"),
]