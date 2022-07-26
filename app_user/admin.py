from django.contrib import admin
from .models import AppUser, UserSearch, TempUser


# Admin for TempUser
class TempUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'otp', 'created_at', 'updated_at')


# Admin Model for AppUser
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'gender', 'created_at', 'updated_at')
    list_filter = ('gender',)


# Admin Model for UserSearch
class UserSearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'search_string', 'searched_at',)
    list_filter = ('search_string', 'user')


# Registering the models
admin.site.register(TempUser, TempUserAdmin)
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(UserSearch, UserSearchAdmin)
