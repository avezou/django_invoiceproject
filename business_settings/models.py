from django.db import models
from address.models import Address


class BusinessInfo(models.Model):
    """
    BusinessInfo model
    This model represents the business issuing the invoice. It is a singleton.
    """
    owner = models.CharField(max_length=255, default="")
    business_name = models.CharField(max_length=255)
    address = models.ForeignKey(Address)
    legal_note = models.TextField(blank=True)
    copyright = models.TextField(blank=True)
    license = models.TextField(blank=True)
    logo = models.ImageField(upload_to='icons', blank=True)

    class Meta:
        verbose_name_plural = 'Business info'

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(BusinessInfo, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()
