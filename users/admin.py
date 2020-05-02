from django.contrib import admin
from users.models import Profile

# Register your models here.
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    inlines = [
        ProfileInline,
    ]