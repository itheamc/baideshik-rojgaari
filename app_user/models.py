from django.db import models
from uuid import uuid4

# App user model
from django.db.models import QuerySet, Q

from foreign_job.models import ForeignJob


# ------------------------------@mit-------------------------------------
# Model for TempUser
class TempUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    otp = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Temp User'
        verbose_name_plural = 'Temp Users'

    def __str__(self):
        return self.email + ' - ' + self.otp


# ------------------------------@mit-------------------------------------
# Model for app user
class AppUser(models.Model):
    GENDER_CHOICES = (('male', 'Male'), ('female', "Female"), ('other', 'Other'))

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='User')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name if self.user.first_name else self.user.username

    class Meta:
        verbose_name = 'App User'
        verbose_name_plural = 'App Users'

    # Property for user search
    @property
    def user_searches(self):
        return self.user_search.all().order_by('-searched_at')

    # Property for user wishlist job
    @property
    def user_wishlist_jobs(self):
        return self.wishlist_job.all().order_by('-created_at')

    # Property for user viewed job
    @property
    def user_viewed_jobs(self):
        return self.viewed_job.all().order_by('-frequency')

    # Property for as_dict
    @property
    def as_dict(self):
        return {
            'id': self.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': self.user.username,
            'email': self.user.email,
            'is_active': self.user.is_active,
            'gender': self.gender,
            'wish_listed_jobs': [job.as_dict for job in self.user_wishlist_jobs if not job.is_trashed]
        }

    # Method to get the jobs as per the user's search queries
    def jobs_as_per_recent_searches(self, limit=20) -> QuerySet[ForeignJob] | None:
        # Getting the app user resent searches data
        searches = self.user_searches[:5]

        # Checking if the user has searched any jobs or not
        if not searches.exists():
            return None

        # Creating search query array from the user searches
        searches_arr = [s.search_string for s in searches]

        # Constructing the query for the jobs as per the recent views
        filter_condition = Q()

        for value in searches_arr:
            filter_condition |= Q(skill_or_title__title__icontains=value)

        # Adding extra query conditions to the query
        filter_condition &= Q(deadline__icontains='days')
        filter_condition &= Q(for_female=self.gender == 'female')

        # Jobs as per your views
        jobs_as_per_searches = ForeignJob.objects.filter(filter_condition).order_by('-deadline')[:limit]

        return jobs_as_per_searches

    # Method to get the jobs as per the user's viewed jobs
    def jobs_as_per_recent_views(self, limit=20) -> QuerySet[ForeignJob] | None:
        # Getting the user recent viewed jobs
        viewed_jobs = self.user_viewed_jobs[:5]

        # Checking if the user has viewed any jobs or not
        if not viewed_jobs.exists():
            return None

        # Creating viewed jobs array from the user viewed jobs
        viewed_jobs_arr = [v.job.skill_or_title.title.lower() for v in viewed_jobs]
        # viewed_jobs_arr_split = [v.split(' ') for v in viewed_jobs_arr]

        # Constructing the query for the jobs as per the recent views
        filter_condition = Q()
        for value in viewed_jobs_arr:
            filter_condition |= Q(skill_or_title__title__icontains=value)

        # Adding extra query conditions to the query
        filter_condition &= Q(deadline__icontains='days')
        filter_condition &= Q(for_female=self.gender == 'female')

        # Jobs as per your views
        jobs_as_per_views = ForeignJob.objects.filter(filter_condition).order_by('-deadline')[:limit]

        return jobs_as_per_views


# ------------------------------@mit-------------------------------------
# User search model
class UserSearch(models.Model):
    user = models.ForeignKey('app_user.AppUser', on_delete=models.SET_NULL, related_name='user_search', null=True)
    search_string = models.CharField(max_length=100)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.search_string

    class Meta:
        verbose_name = 'User Search'
        verbose_name_plural = 'User Searches'
        get_latest_by = 'searched_at'

    # Property for as_dict
    @property
    def as_dict(self):
        return {
            'id': self.id,
            'search_string': self.search_string,
        }
