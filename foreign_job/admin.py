from django.contrib import admin
from .models import Country, JobSkillOrTitle, Company, ForeignJob, UserWishlistJob, UserViewedJob, UserSharedJob


# Admin Model for Country
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'created_at', 'updated_at')


# Model Admin for JobSkillOrTitle
class JobSkillOrTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')


# Model Admin for Company
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')


# Model Admin for ForeignJob
class ForeignJobAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'lot_no', 'skill_or_title', 'company', 'country', 'salary', 'currency', 'deadline',
        'for_female', 'created_at', 'updated_at',)


# Model Admin for Wishlist Jobs
class UserWishlistJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'user', 'is_trashed', 'created_at', 'updated_at')


# Model Admin for UserViewedJob
class UserViewedJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'user', 'frequency', 'first_viewed_at', 'last_viewed_at')
    list_filter = ('user',)


# Model Admin for UserSharedJob
class UserSharedJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'user', 'frequency', 'first_shared_at', 'last_shared_at')
    list_filter = ('user',)


# Registering the models
admin.site.register(Country, CountryAdmin)
admin.site.register(JobSkillOrTitle, JobSkillOrTitleAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(ForeignJob, ForeignJobAdmin)
admin.site.register(UserWishlistJob, UserWishlistJobAdmin)
admin.site.register(UserViewedJob, UserViewedJobAdmin)
admin.site.register(UserSharedJob, UserSharedJobAdmin)
