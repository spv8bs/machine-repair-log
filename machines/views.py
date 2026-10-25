from datetime import timedelta

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from common.mixins import DeleteFormInstanceMixin
from machines.forms import MachineForm, ComponentForm, ComponentDeleteForm
from machines.models import Machine, Component
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



class ComponentCreateView(CreateView):
    model = Component
    form_class = ComponentForm
    template_name = 'machines/components/component_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.machine = get_object_or_404(Machine, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self ):
        initial = super().get_initial()
        initial['machine'] = self.machine
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.machine
        return context

    def get_success_url(self):
        return reverse('machines:detail', kwargs={'pk': self.machine.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Component created successfully')
        return super().form_valid(form)

class ComponentEditView(UpdateView):
    model = Component
    form_class = ComponentForm
    template_name = 'machines/components/component_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.object.machine
        return context

    def get_success_url(self):
        return reverse('machines:detail', kwargs={'pk': self.object.machine.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Component updated successfully')
        return super().form_valid(form)

class ComponentDetailView(DetailView):
    model = Component
    template_name = 'machines/components/component_details.html'

    def get_queryset(self):
        return super().get_queryset().select_related('machine')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repairs = self.object.repairs.select_related('machine').order_by('-detected_on')
        for repair in repairs:
            repair.downtime = calc_downtime(repair.detected_on, repair.downtime_end)
        context['repairs'] = repairs
        return context

class ComponentDeleteView(DeleteFormInstanceMixin, DeleteView):
    model = Component
    form_class = ComponentDeleteForm
    template_name = 'machines/components/component_delete.html'

    def get_success_url(self):
        return reverse('machines:detail', kwargs={'pk': self.object.machine.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Component deleted successfully')
        return super().form_valid(form)