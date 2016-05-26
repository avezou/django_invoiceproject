from django.contrib import admin
from pets.models import Pet, Species
from customers.models import Customer


class SpeciesAdmin(admin.ModelAdmin):
    """
    Edit species information
    """
    list_display = ('species',)
    list_filter = ('species',)
    search_fields = ('species',)


class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'weight', 'owner')
    list_editable = ('age', 'weight')
    list_per_page = 10
    list_max_show_all = 30
    search_fields = ('name', 'weight', 'owner')
    list_filter = ('species', 'age', 'gender', 'weight', 'owner')


admin.site.register(Pet, PetAdmin)
admin.site.register(Species, SpeciesAdmin)
