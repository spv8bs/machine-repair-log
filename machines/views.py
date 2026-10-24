from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from machines.forms import MachineForm
from machines.models import Machine


class MachineListView(ListView):
    model = Machine
    paginate_by = 10
    ordering = 'model'

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