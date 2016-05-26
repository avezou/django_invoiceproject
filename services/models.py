from django.db import models

CHOICES = (
    ('H', 'Hour'),
    ('D', 'Day'),
    ('W', 'Week')
)


class Service(models.Model):
    """
    Service model
    Hold iformation pertinent to the type of service. Modify as necessary for
    your use case
    """
    type_of_service = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2,
                                verbose_name="Price ($):")
    per = models.CharField(max_length=1, choices=CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.type_of_service
