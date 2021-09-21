from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Stylist, Client, ServiceOffering, ProductOffering, City, Region, Review

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'is_stylist',
            'is_client',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'name', 'is_client', 'is_stylist', 'is_staff')
    list_filter = ('groups',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
admin.site.register(Stylist)
admin.site.register(Client)
admin.site.register(ServiceOffering)
admin.site.register(ProductOffering)
admin.site.register(City)
admin.site.register(Region)
admin.site.register(Review)
