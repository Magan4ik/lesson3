from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, Profile, Follow


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'register_token')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth')
    list_filter = ('gender', 'date_of_birth')
    search_fields = ('user',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('author', 'user',)
    list_filter = ('author', 'created')