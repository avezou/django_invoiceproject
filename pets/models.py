from django.db import models


GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', "Other"),
)


class Species(models.Model):
    """
    Very simple model to handle different species. Could be expanded to add
    more information or customized appropriately based on goods
    """
    species = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = 'Species'

    def __str__(self):
        return self.species


class Pet(models.Model):
    """
    Pet model
    Holds information pertinent to pets. Owner is a TextField to hold the owner's
    name. This helps when it comes time to display information. 
    """
    species = models.ForeignKey(Species)
    name = models.CharField(max_length=50)
    weight = models.DecimalField(
        "Weight (lbs)",
        max_digits=5,
        decimal_places=2)
    age = models.IntegerField("Age (months)")
    gender = models.CharField(max_length=1, choices=GENDER)
    owner = models.CharField(max_length=30, help_text="Owner's last name")
    additional_info = models.TextField(
        max_length=500,
        help_text="Eating, walking, sleeping habits and more")

    def __str__(self):
        return "%s (%s's %s)" % (self.name, self.owner, self.species.species)
