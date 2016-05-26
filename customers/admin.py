from django.contrib import admin
from customers.models import Customer


class PetInline(admin.TabularInline):
    """
    Inline admin to add pets to customers
    """
    model = Customer.pets.through


class CustomerAdmin(admin.ModelAdmin):
    """
    Add and edit customer info here
    """
    # from django.utils.html import format_html
    list_display = ('last_name', 'first_name', 'send_email')
    search_fields = ('first_name', 'last_name', 'email')
    inlines = [
        PetInline,
    ]


admin.site.register(Customer, CustomerAdmin)
