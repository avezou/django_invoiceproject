from django.contrib import admin
from customers.models import Customer, Address
from .forms import ZipAdminForm


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


class AddressAdmin(admin.ModelAdmin):
    """
    Customize address forms and display here
    """
    form = ZipAdminForm
    list_display = ('state', 'city', 'address_1',)
    list_filter = ('city', 'state', 'zip_code',)
    search_fields = ('address_1', 'city', 'state', 'zip_code')

    def get_changelist_form(self, request, **kwargs):
        return ZipAdminForm


admin.site.register(Address, AddressAdmin)
admin.site.register(Customer, CustomerAdmin)
