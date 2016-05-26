from django.contrib import admin
from services.models import Service


class ServiceAdmin(admin.ModelAdmin):
    """
    Edit services 
    """
    list_display = ('type_of_service', 'price', 'per')
    list_editable = ('price', 'per')
    list_per_page = 10
    list_max_show_all = 30
    search_fields = ('type_of_service',)
    list_filter = ('price', 'type_of_service', 'per')


admin.site.register(Service, ServiceAdmin)
