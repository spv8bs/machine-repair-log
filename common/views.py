from django.views.generic import TemplateView

from machines.models import Machine
from repairs.models import Repair


class HomePageView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machines_count'] = Machine.objects.count()
        context['repairs_count'] = Repair.objects.count()
        context['open_repairs_count'] =   Repair.objects.filter(
            resolved_on__isnull=True, limited_on__isnull=True).count()
        context['latest_repairs'] = (
            Repair.objects.select_related('machine', 'component').order_by('-detected_on')[:5]
        )
        return context
