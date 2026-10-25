from datetime import timedelta

from django.contrib import messages
from django.db.models import Count
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from machines.forms import MachineForm
from machines.models import Machine
from common.utils import calc_downtime


class MachineListView(ListView):
    model = Machine
    paginate_by = 10
    paginate_orphans = 3
    ordering = 'model'

    # calculate qty repairs per machine
    def get_queryset(self):
        return super().get_queryset().annotate(repairs_count=Count('repairs'))

class MachineCreateView(CreateView):
    model = Machine
    form_class = MachineForm
    template_name = 'machines/machine_create.html'
    success_url = reverse_lazy('machines:list')

    def form_valid(self, form):
        messages.success(self.request, 'Machine created successfully')
        return super().form_valid(form)


class MachineDetailView(DetailView):
    model = Machine
    template_name = 'machines/machine_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repairs = self.object.repairs.select_related('component').order_by('-detected_on')

        now = timezone.now()
        total_downtime = timedelta()
        total_cost = 0
        open_count = 0

        for repair in repairs:
            repair.downtime = calc_downtime(repair.detected_on, repair.downtime_end)
            total_downtime += (repair.downtime_end or now) - repair.detected_on
            total_cost += repair.cost
            if not repair.is_resolved:
                open_count += 1

        context['repairs'] = repairs
        context['repairs_count'] = len(repairs)
        context['open_repairs_count'] = open_count
        context['total_downtime'] = calc_downtime(now - total_downtime, now)
        context['total_cost'] = total_cost
        return context

class MachineEditView(UpdateView):
    model = Machine
    form_class = MachineForm
    template_name = 'machines/machine_edit.html'

    def get_success_url(self):
        return reverse_lazy('machines:list') #kwargs={'pk':self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Machine updated successfully')
        return super().form_valid(form)


class MachineDeleteView(DeleteView):
    model = Machine
    template_name = 'machines/machine_delete.html'
    success_url = reverse_lazy('machines:list')

    def form_valid(self, form):
        messages.success(self.request, 'Machine deleted successfully')
        return super().form_valid(form)

    # TODO да изнеса в mixin message.success