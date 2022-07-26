from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jobs/', include('foreign_job.urls')),
    path('user/', include('app_user.urls'))
]

