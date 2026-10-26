import re

from django.contrib import messages
from django.db.models import Prefetch, Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView

from machines.models import Machine
from common.mixins import DeleteFormInstanceMixin
from repairs.forms import RepairForm, RepairActionForm, RepairDeleteForm, RepairSearchForm, RepairActionDeleteForm
from repairs.models import Repair, RepairAction
from common.utils import repair_stats

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
            status = self.form.cleaned_data['status']
            if machine:
                queryset = queryset.filter(machine=machine)

            status_filters = {
                'open': Q(resolved_on__isnull=True, limited_on__isnull=True),
                'limited': Q(resolved_on__isnull=True, limited_on__isnull=False),
                'resolved': Q(resolved_on__isnull=False),
            }
            if status:
                queryset = queryset.filter(status_filters[status])

            # search in repair No., component, problem ... X diagnosis
            if query:
                number_match = re.fullmatch(r'R-(\d{4})(?:-(\d*))?', query, re.IGNORECASE)
                if number_match:
                    # search by repair number or year
                    year, number = number_match.groups()
                    search = Q(detected_on__year=int(year))
                    if number:
                        search &= Q(pk=int(number))
                else:
                    search = Q(problem__icontains=query) | Q(component__component_type__icontains=query)
                    if query.isdigit():
                        search |= Q(pk=int(query))
                        if len(query) == 4:
                            search |= Q(detected_on__year=int(query))

                queryset = queryset.filter(search)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        # for repair in context['repairs']:
        #     repair.downtime = calc_downtime(repair.detected_on, repair.downtime_end)
        context.update(repair_stats(self.object_list))
        return context


class RepairCreateView(CreateView):
    model = Repair
    form_class = RepairForm
    template_name = 'repairs/repair_create.html'
    success_url = reverse_lazy('repairs:list')

    def dispatch(self, request, *args, **kwargs):
        machine_pk = request.GET.get('machine', '')
        # return 500 -> resolved
        if not machine_pk.isdigit():
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
        # repair = context['repair']
        # repair.downtime = calc_downtime(repair.detected_on, repair.downtime_end)
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

class RepairActionEditView(UpdateView):
    model = RepairAction
    form_class = RepairActionForm
    template_name = 'repairs/repair_action_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['repair'] = self.object.repair
        return context

    def get_success_url(self):
        return reverse('repairs:detail', kwargs={'pk': self.object.repair.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Action edited successfully')
        return super().form_valid(form)

class RepairActionDeleteView(DeleteFormInstanceMixin, DeleteView):
    model = RepairAction
    form_class = RepairActionDeleteForm
    template_name = 'repairs/repair_action_delete.html'

    def get_success_url(self):
        return reverse('repairs:detail', kwargs={'pk': self.object.repair.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Action deleted successfully')
        return super().form_valid(form)


