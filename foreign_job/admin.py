from django.contrib import admin
from .models import ForeignJob


# Admin Model for ForeignJob
class ForeignJobAdmin(admin.ModelAdmin):
    list_display = (
        'lot_no', 'skill_name', 'company_name', 'country_name', 'salary', 'currency', 'deadline', 'for_female')

    list_filter = ('skill_name', 'for_female')


# Registering the models
admin.site.register(ForeignJob, ForeignJobAdmin)
