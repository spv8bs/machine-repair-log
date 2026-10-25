from django.contrib import messages
from django.db.models import Prefetch, Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView

from machines.models import Machine
from common.mixins import DeleteFormInstanceMixin
from repairs.forms import RepairForm, RepairActionForm, RepairDeleteForm, RepairSearchForm
from repairs.models import Repair, RepairAction
from common.utils import calc_downtime


class RepairSelectMachineView(TemplateView):
    template_name = 'repairs/select_machine.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machines'] = Machine.objects.order_by('model')
        return context

class RepairListView(ListView):
    model = Repair
    template_name = 'repairs/repair_list.html'
    context_object_name = 'repairs'
    ordering = ['-detected_on']
    paginate_by = 10
    paginate_orphans = 3

    def get_queryset(self):
        queryset = super().get_queryset().select_related('machine', 'component')

        self.form = RepairSearchForm(self.request.GET)
        if self.form.is_valid():
            machine = self.form.cleaned_data['machine']
            query = self.form.cleaned_data['query']
            if machine:
                queryset = queryset.filter(machine=machine)
            # search in component, problem ... X diagnosis
            if query:
                queryset = queryset.filter(
                    Q(problem__icontains=query) #| Q(diagnosis__icontains=query)
                    | Q(component__component_type__icontains=query)
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        for repair in context['repairs']:
            repair.downtime = calc_downtime(repair.detected_on, repair.downtime_end)
        return context


class RepairCreateView(CreateView):
    model = Repair
    form_class = RepairForm
    template_name = 'repairs/repair_create.html'
    success_url = reverse_lazy('repairs:list')

    def dispatch(self, request, *args, **kwargs):
        machine_pk = request.GET.get('machine', '')
        if not machine_pk:
            return redirect('repairs:select_machine')
        self.machine = get_object_or_404(Machine, pk=machine_pk)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['machine'] = self.machine
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.machine
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Repair created successfully')
        return super().form_valid(form)


class RepairDetailView(DetailView):
    model = Repair
    template_name = 'repairs/repair_details.html'

    def get_queryset(self):
        actions = RepairAction.objects.select_related('technician').order_by('created_at')
        return (
            super().get_queryset().select_related('machine', 'component')
            .prefetch_related('technicians', 'parts', Prefetch('actions', queryset=actions))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repair = context['repair']
        repair.downtime = calc_downtime(repair.detected_on, repair.downtime_end)
        return context

class RepairEditView(UpdateView):
    model = Repair
    form_class = RepairForm
    template_name = 'repairs/repair_edit.html'

    def get_success_url(self):
        return reverse('repairs:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Repair edited successfully')
        return super().form_valid(form)


class RepairDeleteView(DeleteFormInstanceMixin, DeleteView):
    model = Repair
    form_class = RepairDeleteForm
    template_name = 'repairs/repair_delete.html'
    success_url = reverse_lazy('repairs:list')

    def form_valid(self, form):
        messages.success(self.request, 'Repair deleted successfully')
        return super().form_valid(form)



class RepairActionCreateView(CreateView):
    model = RepairAction
    form_class = RepairActionForm
    template_name = 'repairs/repair_action_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.repair = get_object_or_404(Repair, pk=kwargs['repair_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['repair'] = self.repair
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['repair'] = self.repair
        return context

    def get_success_url(self):
        return reverse('repairs:detail', kwargs={'pk': self.repair.pk})

    def form_valid(self, form):
        form.instance.repair = self.repair
        messages.success(self.request, 'Action created successfully')
        return super().form_valid(form)

