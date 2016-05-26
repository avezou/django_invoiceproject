from django.contrib import admin
from django.template.loader import render_to_string
from business_settings.models import BusinessInfo

from sorl.thumbnail import default
ADMIN_THUMBS_SIZE = '60x60'


class BusinessAdmin(admin.ModelAdmin):
    """
    Edit business information here.
    """
    list_display = ('business_name', 'address', 'owner', 'image_thumb')

    def image_thumb(self, obj):
        if obj.logo:
            thumb = default.backend.get_thumbnail(obj.logo.file,
                                                  ADMIN_THUMBS_SIZE)
            return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
        else:
            return "No Image"
    image_thumb.short_description = 'Logo'
    image_thumb.allow_tags = True


admin.site.register(BusinessInfo, BusinessAdmin)
