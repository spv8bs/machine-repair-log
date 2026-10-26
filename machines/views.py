from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from common.mixins import DeleteFormInstanceMixin
from machines.forms import MachineForm, ComponentForm, ComponentDeleteForm, MachineFilterForm
from machines.models import Machine, Component
from common.utils import repair_stats


class MachineListView(ListView):
    model = Machine
    paginate_by = 10
    paginate_orphans = 3
    ordering = 'model'

    # calculate qty repairs per machine
    def get_queryset(self):
        queryset = super().get_queryset().annotate(repairs_count=Count('repairs'))

        # filter by location
        self.form = MachineFilterForm(self.request.GET)
        if self.form.is_valid() and self.form.cleaned_data['location']:
            queryset = queryset.filter(location__iexact=self.form.cleaned_data['location'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

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
        context['repairs'] = repairs
        context.update(repair_stats(repairs))
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
        if self.object.repairs.exists():
            messages.error(self.request,
                           'This machine has repairs and cannot be deleted. Delete its repairs first or mark it as inactive.')
            return redirect('machines:detail', pk=self.object.pk)
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
        # for repair in repairs:
        #     repair.downtime = calc_downtime(repair.detected_on, repair.downtime_end)
        context['repairs'] = repairs
        context.update(repair_stats(repairs))
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