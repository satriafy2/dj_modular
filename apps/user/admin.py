from django.contrib import admin
from apps.user.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


# class UserAdmin(admin.ModelAdmin):
#     pass

class DefUserAdmin(DefaultUserAdmin):
    fieldsets = (
        *DefaultUserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Custom Field Heading',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'role',
                    'company'
                ),
            },
        ),
    )


# admin.site.register(User, UserAdmin)
admin.site.register(User, DefUserAdmin)

