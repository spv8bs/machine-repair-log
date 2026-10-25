from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from common.mixins import DeleteFormInstanceMixin
from resources.forms import TechnicianForm, TechnicianDeleteForm, SupplierForm, SupplierDeleteForm, PartForm, \
    PartDeleteForm
from resources.models import Technician, Supplier, Part


# Technician Views

class TechnicianListView(ListView):
    model = Technician
    template_name = 'resources/technician/technician_list.html'
    ordering = ['first_name', 'last_name']

class TechnicianCreateView(CreateView):
    model = Technician
    form_class = TechnicianForm
    template_name = 'resources/technician/technician_create.html'
    success_url = reverse_lazy('resources:technician_list')

    def form_valid(self, form):
        messages.success(self.request, 'Technician created successfully')
        return super().form_valid(form)

class TechnicianEditView(UpdateView):
    model = Technician
    form_class = TechnicianForm
    template_name = 'resources/technician/technician_edit.html'

    def get_success_url(self):
        return reverse('resources:technician_details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Technician updated successfully')
        return super().form_valid(form)

class TechnicianDeleteView(DeleteFormInstanceMixin, DeleteView):
    model = Technician
    form_class = TechnicianDeleteForm
    template_name = 'resources/technician/technician_delete.html'
    success_url = reverse_lazy('resources:technician_list')

    def form_valid(self, form):
        messages.success(self.request, 'Technician deleted successfully')
        return super().form_valid(form)

class TechnicianDetailView(DetailView):
    model = Technician
    template_name = 'resources/technician/technician_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['repairs'] = (self.object.repairs.select_related('machine', 'component')
                              .order_by('-detected_on'))
        return context


# Supplier Views

class SupplierListView(ListView):
    model = Supplier
    template_name = 'resources/supplier/supplier_list.html'
    ordering = ['name']
    paginate_by = 10
    paginate_orphans = 3

class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'resources/supplier/supplier_create.html'
    success_url = reverse_lazy('resources:supplier_list')

    def form_valid(self, form):
        messages.success(self.request, 'Supplier created successfully')
        return super().form_valid(form)

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'resources/supplier/supplier_details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parts'] = self.object.parts.order_by('name')
        return context

class SupplierEditView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'resources/supplier/supplier_edit.html'

    def get_success_url(self):
        return reverse('resources:supplier_details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Supplier updated successfully')
        return super().form_valid(form)

class SupplierDeleteView(DeleteFormInstanceMixin, DeleteView):
    model = Supplier
    form_class = SupplierDeleteForm
    template_name = 'resources/supplier/supplier_delete.html'
    success_url = reverse_lazy('resources:supplier_list')
    def form_valid(self, form):
        messages.success(self.request, 'Supplier deleted successfully')
        return super().form_valid(form)


# Part Views

class PartListView(ListView):
    model = Part
    template_name = 'resources/part/part_list.html'
    paginate_by = 10
    paginate_orphans = 3
    ordering = ['name']

    def get_queryset(self):
        return super().get_queryset().select_related('supplier')

class PartCreateView(CreateView):
    model = Part
    form_class = PartForm
    template_name = 'resources/part/part_create.html'
    success_url = reverse_lazy('resources:part_list')

    def form_valid(self, form):
        messages.success(self.request, 'Part created successfully')
        return super().form_valid(form)

class PartDeleteView(DeleteFormInstanceMixin, DeleteView):
    model = Part
    form_class = PartDeleteForm
    template_name = 'resources/part/part_delete.html'
    success_url = reverse_lazy('resources:part_list')

    def form_valid(self, form):
        messages.success(self.request, 'Part deleted successfully')
        return super().form_valid(form)

class PartEditView(UpdateView):
    model = Part
    form_class = PartForm
    template_name = 'resources/part/part_edit.html'

    def get_success_url(self):
        return reverse('resources:part_details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Part updated successfully')
        return super().form_valid(form)

class PartDetailView(DetailView):
    model = Part
    template_name = 'resources/part/part_details.html'

    def get_queryset(self):
        return super().get_queryset().select_related('supplier')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['repairs'] = (self.object.repairs.select_related('machine', 'component')
                              .order_by('-detected_on'))
        return context