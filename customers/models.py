from django.db import models
from localflavor.us.models import USStateField
from localflavor.us.models import PhoneNumberField
from django.contrib.gis.db import models as models2
from django.utils.translation import ugettext as _

from pets.models import Pet
from django_simple_address import Address


class Customer(models.Model):
    """
    Customer model
    Holds customer information. Pets here is not necessary, but this is a specific
    implementations, so I added it. It can be replaced with whatever your business
    caters to, or removed completely (other parts of the code would have to be
    modified as well)
    """
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    pets = models.ManyToManyField(Pet, through='PetServiced')
    address = models.ForeignKey(Address)
    email = models.EmailField()

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)

    def send_email(self):
        from django.utils.html import mark_safe
        return mark_safe('<a class="grp-button" href="mailto:%s?Subject=OnTheMovePetCare communications" target="_top">Email</a>' %
                         self.email)


class PetServiced(models.Model):
    """
    Through model to handle the ManyToMany relation between customer and pets
    """
    customer = models.ForeignKey(Customer)
    pet = models.ForeignKey(Pet)

    class Meta:
        verbose_name = 'Pet'

    def __str__(self):
        return 'Pets'
