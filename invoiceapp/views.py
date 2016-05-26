from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'invoiceapp/index.html'
