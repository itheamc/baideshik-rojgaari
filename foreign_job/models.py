from django.db import models
from django.db.models import QuerySet, Q


# Country model
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    # Property for as_dict
    @property
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code
        }


# Model for job title/position/skills
class JobSkillOrTitle(models.Model):
    title = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='job_skills_or_titles', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # Property for as_dict
    @property
    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image.url if self.image else None
        }

    class Meta:
        verbose_name = 'Job Skill Or Title'
        verbose_name_plural = 'Job Skills Or Titles'


# Model for Company
class Company(models.Model):
    name = models.CharField(max_length=240, unique=True)
    logo = models.ImageField(upload_to='companies', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # Property for as_dict
    @property
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo': self.logo.url if self.logo else None
        }

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


# Model for the jobs table
class ForeignJob(models.Model):
    row_total = models.IntegerField()
    lot_detail_id = models.IntegerField(unique=True)
    lot_no = models.CharField(max_length=20)
    skill_or_title = models.ForeignKey('foreign_job.JobSkillOrTitle', on_delete=models.SET_NULL, null=True,
                                       related_name='foreign_jobs')
    country = models.ForeignKey('foreign_job.Country', on_delete=models.SET_NULL, null=True, related_name='jobs')
    company = models.ForeignKey('foreign_job.Company', on_delete=models.SET_NULL, null=True, related_name='jobs')
    salary = models.CharField(max_length=100)
    currency = models.CharField(max_length=20)
    deadline = models.CharField(max_length=100)
    deadline_date = models.CharField(max_length=100)
    for_female = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.skill_or_title.title if self.skill_or_title else self.lot_no

    # Property for skill_name
    @property
    def skill_name(self):
        return self.skill_or_title.title if self.skill_or_title else "Unknown"

    # Property for as_dict
    @property
    def as_dict(self):
        return {
            'id': self.id,
            'row_total': self.row_total,
            'lot_detail_id': self.lot_detail_id,
            'lot_no': self.lot_no,
            'skill_or_title': self.skill_or_title.as_dict if self.skill_or_title else None,
            'company': self.company.as_dict if self.company else None,
            'country': self.country.as_dict if self.country else None,
            'salary': self.salary,
            'currency': self.currency,
            'deadline': self.deadline,
            'deadline_date': self.deadline_date,
            'for_female': self.for_female
        }

    # Property for as_dict
    @property
    def as_dict_without_country(self):
        return {
            'id': self.id,
            'row_total': self.row_total,
            'lot_detail_id': self.lot_detail_id,
            'lot_no': self.lot_no,
            'skill_or_title': self.skill_or_title.as_dict if self.skill_or_title else None,
            'company': self.company.as_dict if self.company else None,
            'salary': self.salary,
            'currency': self.currency,
            'deadline': self.deadline,
            'deadline_date': self.deadline_date,
            'for_female': self.for_female
        }

    # Method to apply filters
    @staticmethod
    def apply_filters(filters=None, limit=100, offset=0) -> QuerySet:
        # Constructing the query for the jobs as per the filters
        filter_condition = Q()

        for key, value in filters.items():
            filter_condition &= Q(**{key: value})

        # Jobs after applying the filters
        jobs = ForeignJob.objects.filter(filter_condition).order_by('-deadline')[offset:limit]

        return jobs

    class Meta:
        verbose_name = 'Foreign Job'
        verbose_name_plural = 'Foreign Jobs'


# User Wishlist Job model
class UserWishlistJob(models.Model):
    job = models.ForeignKey('foreign_job.ForeignJob', on_delete=models.CASCADE, related_name='wishlist_job')
    user = models.ForeignKey('app_user.AppUser', on_delete=models.CASCADE, related_name='wishlist_job')
    is_trashed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job.skill_name

    class Meta:
        verbose_name = 'User Wishlist Job'
        verbose_name_plural = 'User Wishlist Jobs'

    # Property for as_dict
    @property
    def as_dict(self):
        return {
            'id': self.id,
            'job': self.job.as_dict,
            'is_trashed': self.is_trashed,
        }


# User Viewed Job model
class UserViewedJob(models.Model):
    job = models.ForeignKey('foreign_job.ForeignJob', on_delete=models.CASCADE, related_name='viewed_job')
    user = models.ForeignKey('app_user.AppUser', on_delete=models.CASCADE, related_name='viewed_job')
    frequency = models.IntegerField(default=1)
    first_viewed_at = models.DateTimeField(auto_now_add=True)
    last_viewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job.skill_name

    class Meta:
        verbose_name = 'User Viewed Job'
        verbose_name_plural = 'User Viewed Jobs'

    # Property for as_dict
    @property
    def as_dict(self):
        return {
            'id': self.id,
            'job': self.job.as_dict,
            'frequency': self.frequency,
        }


# User Shared Job model
class UserSharedJob(models.Model):
    job = models.ForeignKey('foreign_job.ForeignJob', on_delete=models.CASCADE, related_name='shared_job')
    user = models.ForeignKey('app_user.AppUser', on_delete=models.CASCADE, related_name='shared_job')
    frequency = models.IntegerField(default=1)
    first_shared_at = models.DateTimeField(auto_now_add=True)
    last_shared_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job.skill_name

    class Meta:
        verbose_name = 'User Shared Job'
        verbose_name_plural = 'User Shared Jobs'

    # Property for as_dict
    @property
    def as_dict(self):
        return {
            'id': self.id,
            'job': self.job.as_dict,
            'frequency': self.frequency,
        }
