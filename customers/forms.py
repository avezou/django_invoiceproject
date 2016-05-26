from django import forms
from .models import Address
from localflavor.us.forms import USZipCodeField


class ZipAdminForm(forms.ModelForm):

    class Meta:
        model = Address
        widget = {
            'zip_code': USZipCodeField(),
        }
        fields = (
            'address_1',
            'address_2',
            'city',
            'state',
            'zip_code',
            'phone_number',
            'customer_name')
