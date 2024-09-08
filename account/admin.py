from django.contrib import admin

# Register your models here.
from .models import AUser
from django.contrib.auth.admin import UserAdmin

class UserModelAdmin(UserAdmin):

  # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "name","tc","is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("Usercredientials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name","tc"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
 
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserModelAdmin...
admin.site.register(AUser, UserModelAdmin)