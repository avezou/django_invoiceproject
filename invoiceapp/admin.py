import os
from django.contrib import admin

from django.utils.html import format_html
from django.contrib import messages


from .models import Invoice, ServiceQuantity
from customers.models import Customer
from business_settings.models import BusinessInfo
from .invoice import generate_invoice


class ServiceInline(admin.TabularInline):
    """
    Inline to add services to an invoice
    """
    model = ServiceQuantity
    extra = 1

#
# class CustomerInLine(admin.TabularInline):
#     model = Customer
#     extra = 0


class InvoiceAdmin(admin.ModelAdmin):
    """
    Admin file to manipulte invoices
    Generation of the invoice file, as well as sending email to customers, is
    done using django actions on the admin page
    """
    list_display = ('invoice_title',
                    'date_billed', 'date_due', 'customer', 'ready_to_send', 'email_sent',
                    'pdf_link')
    readonly_fields = ['invoice_title', 'id', 'date_created', 'invoice_file',
                       'email_sent', 'invoice_total']
    search_fields = ('invoice_title', 'date_billed', 'date_due',
                     'date_created', 'customer__last_name',
                     'customer__first_name')
    # list_display_links = ('invoice_title', 'invoice_file')
    list_filter = ('date_created', 'date_billed', 'date_due', 'customer__last_name',
                   'customer__first_name', 'email_sent')
    inlines = [
        ServiceInline,
    ]
    exclude = ('services',)
    actions = ['email_customers', 'clear_mail_flag', 'calculate_total']

    def email_customers(modeladmin, request, queryset):
        """
        Send email with pdf invoice attached to customers.
        The template for the email is /invoiceapp/templates/invoiceapp/email.html
        """
        from django.core.mail import send_mail, EmailMessage
        from django.template.loader import get_template
        from django.template import Context
        busInfo = BusinessInfo.objects.all()[0]
        add2 = '\n' + busInfo.address.address_2 + \
            '\n' if busInfo.address.address_2 else '\n'
        for invoice in queryset:
            ctx = {
                'user': invoice.customer.first_name,
                'business': busInfo.business_name,
                'owner': busInfo.owner,
                'add1': busInfo.address.address_1,
                'add2': add2,
                'locality': busInfo.address.city + ', ' + busInfo.address.state + ' ' + busInfo.address.zip_code,
                'phone': busInfo.address.phone_number
            }
            message = get_template(
                'invoiceapp/email.html').render(Context(ctx))
            email = EmailMessage('Invoice from ' + busInfo.business_name + ' due on ' +
                                 invoice.date_due.strftime("%A %d %Y"),
                                 message,
                                 request.user.email,
                                 [invoice.customer.email],
                                 reply_to=[request.user.email])
            #  headers={'Message-ID': 'foo'})
            email.content_subtype = "html"
            email.attach_file(invoice.invoice_file.path)

            if invoice.ready_to_send:
                if email.send(fail_silently=False):
                    invoice.email_sent = True
                    invoice.ready_to_send = True
                    # invoice.save()
                    queryset.update(email_sent=True, ready_to_send=True)
                    messages.add_message(request, messages.INFO,
                                         'Email sent successfully')
            else:
                messages.add_message(request, messages.ERROR,
                                     'Email not sent, total not calculated for invoice %s' % invoice.invoice_title)

    def calculate_total(modeladmin, request, queryset):
        """
        Calculates the total for this invoice and generates the invoice file
        """
        for invoice in queryset:
            total_price = 0.0
            services = invoice.services.all()
            for service in services:
                serq = ServiceQuantity.objects.get(
                    invoice=invoice, service=service)
                total_price += float(serq.total_price)
                print("serq val: " + str(serq.total_price))
                print("Total in calc tot: " + str(total_price))
            invoice.invoice_total = total_price

            if invoice.invoice_total > 0.00:
                invoice.ready_to_send = True
                # invoice.save()
                queryset.update(invoice_total=total_price, ready_to_send=True)
                invoices_dir = os.path.join('invoiceapp', 'invoices')
                makedirs(invoices_dir)
                file_path = os.path.join(
                    invoices_dir, invoice.invoice_title + '.pdf')
                if os.path.isfile(invoice.invoice_file.path):
                    os.remove(invoice.invoice_file.path)
                generate_invoice(invoice, services, os.path.join('media', file_path))
                messages.add_message(request, messages.INFO,
                                     'Total calculated successfully')
            else:
                messages.add_message(request, messages.ERROR,
                                     'Total not calculated successfully')

    calculate_total.short_description = 'Generate invoice'

    def clear_mail_flag(modeladmin, request, queryset):
        """
        Clear the email sent flag
        """
        for invoice in queryset:
            if invoice.email_sent:
                invoice.email_sent = False
                invoice.ready_to_send = False
                invoice.save()
                queryset.update(email_sent=False)

    def save_model(self, request, obj, form, change):
        """
        Override the admin save_model to customize messages and perform post_save
        actions
        """
        bus = BusinessInfo.objects.all()
        if len(bus) == 0:
            messages.set_level(request, messages.ERROR)
            messages.add_message(request, messages.ERROR,
                                 'Invoice not saved. Make sure to create business info first')
        else:
            obj.email_sent = False
            obj.ready_to_send = False
            if obj.invoice_file and os.path.isfile(obj.invoice_file.path):
                os.remove(obj.invoice_file.path)
            obj.save()
            # super(InvoiceAdmin, self).save_model(request, obj, form, change)

    clear_mail_flag.short_description = "Email not sent"
    email_customers.short_description = "Send bill to customer"


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == 17:
            # Dir already exists. No biggie.
            pass


admin.site.register(Invoice, InvoiceAdmin)
