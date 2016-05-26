import uuid
import os

from decimal import Decimal

from django.db import models
from django.core.files import File
from django.utils.timezone import datetime, timedelta

from services.models import Service
from customers.models import Customer
from business_settings.models import BusinessInfo


def auto_due_date():
    return datetime.today() + timedelta(days=30)


class Invoice(models.Model):
    """
    Invoice model
    This model contains the fields necessary to hangle the invoice for a
    service based small business. It relys on the Service, Customer, and
    BusinessInfo models to fill in the fields necessary for a reportlab
    invoice generation
    """
    invoice_title = models.CharField(max_length=255, verbose_name='Invoice',
                                     editable=False, default='')
    date_created = models.DateField(auto_now=True)
    date_billed = models.DateField(default=datetime.today)
    date_due = models.DateField(default=auto_due_date)
    services = models.ManyToManyField(Service, through='ServiceQuantity')
    customer = models.ForeignKey(Customer)
    invoice_file = models.FileField(blank=True, null=True, editable=False)
    email_sent = models.BooleanField(default=False, editable=False)
    ready_to_send = models.BooleanField(default=False, editable=False)
    invoice_total = models.DecimalField(max_digits=10, decimal_places=2,
                                        default=Decimal('0.00'))

    def __str__(self):
        return self.invoice_title

    def pdf_link(self):
        from django.utils.html import mark_safe
        print("invoice url: " + self.invoice_file.url)
        if '_invoice_' in self.invoice_file.url and self.ready_to_send:
            return mark_safe('<a class="grp-button" href="%s" target="blank">View invoice</a>' %
                             self.invoice_file.url)
        else:
            return mark_safe(
                '<a class="btn btn-danger" href="#">Invoice not ready</a>')

    pdf_link.short_description = "Invoice File"

    def save(self, *args, **kwargs):
        # Need to add arguments to generate to make it
        # customizable based on the object
        invoices_dir = os.path.join('invoiceapp', 'invoices')
        # makedirs(invoices_dir)
        file_path = os.path.join(invoices_dir, self.invoice_title + '.pdf')
        busInfo = BusinessInfo.objects.all()
        if len(busInfo) > 0:

            self.invoice_total = 0.00
            self.email_sent = False
            self.ready_to_send = False
            super(Invoice, self).save(*args, **kwargs)
            self.invoice_title = self.date_billed.strftime(
                "%Y_%m_%d") + "_" + self.customer.last_name.replace(' ', '_') + "_invoice_" + str(self.id)
            self.invoice_file = file_path
            # generate(self, os.path.join('media', file_path))
            # services = ServiceQuantity.objects.filter(invoice=self)
            # # i = Invoice.objects.get(invoice_title=self.invoice_title)
            # # services = i.service_quantities.all()
            # # print ("Outside for")
            # for service in services:
            #     self.invoice_total += float(service.total_price)

            super(Invoice, self).save(*args, **kwargs)


class ServiceQuantity(models.Model):
    """
    ServiceQuantity model
    This is a through model used in the ManyToMany relations between invoice
    and services.
    """
    invoice = models.ForeignKey(Invoice, related_name='service_quantities')
    service = models.ForeignKey(Service)
    quantity = models.DecimalField(max_digits=4, decimal_places=2,
                                   default=Decimal('0.00'),
                                   verbose_name="Duration:")
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                default=Decimal('0.00'),
                                verbose_name="Price:")
    total_price = models.DecimalField(max_digits=6, decimal_places=2,
                                      default=Decimal('0.00'),
                                      verbose_name="Total price:")

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        auto_created = True

    def __str__(self):
        return "Services"

    def save(self, *args, **kwargs):
        self.price = self.service.price
        self.total_price = self.service.price * self.quantity
        busInfo = BusinessInfo.objects.all()
        if len(busInfo) > 0:
            super(ServiceQuantity, self).save(*args, **kwargs)


# def makedirs(path):
#     try:
#         os.makedirs(path)
#     except OSError as e:
#         if e.errno == 17:
#             # Dir already exists. No biggie.
#             pass
