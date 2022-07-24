from django.apps import AppConfig


class JobsUpdaterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs_updater'

    # def ready(self):
    #     from . import schedular
    #     schedular.start()
