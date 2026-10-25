from django import forms
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from common.mixins import DisabledFormMixin, BootstrapFormMixin
from machines.models import Component, Machine
from repairs.models import Repair, RepairAction


class RepairForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Repair
        fields = '__all__'
        labels = {
            'machine': 'Machine',
            'component': 'Component',
            'problem': 'Problem',
            'detected_on': 'Detected on',
            'resolved_on': 'Resolved on',
            'limited_on': 'Limited since',
            'diagnosis': 'Diagnosis',
            'cost': 'Cost',
            'photo': 'Photo',
            'technicians': 'Technicians',
            'parts': 'Parts used'
        }
        help_texts = {
            'component': 'Choose a component of the selected machine, or leave empty if it is not related to a specific component',
            'resolved_on': 'Leave empty while the repair is still open',
            'limited_on': 'If machine runs with limitations, but the repair is not finished',
            'cost': 'Total cost of the repair',
            'technicians': 'Technicians of the repair (hold Ctrl to select more than one)',
            'parts': 'Parts of the repair (hold Ctrl to select more than one)'
        }
        error_messages = {
            'machine': {'required': 'Please select a machine'}

        }

        widgets = {
            'problem': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Describe problem'}),
            'detected_on': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'),
            'resolved_on': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'),
            'limited_on': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'),
            'diagnosis': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Diagnosis'}),
            'cost': forms.NumberInput(
                attrs={'min': 0, 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['machine'].disabled = True

        # if self.instance.pk:
        #     selected_machine = self.instance.machine
        # else:
        #     selected_machine = self.initial.get('machine')
        selected_machine = self.instance.machine if self.instance.pk else self.initial.get('machine')

        components = Component.objects.select_related('machine').order_by('machine__model', 'component_type')
        # machine filtered components -> TODO for future - dynamic filtered list with JavaShit?? without block machine field
        if selected_machine:
            components = components.filter(machine=selected_machine)
        self.fields['component'].queryset = components
        if selected_machine and not isinstance(self, DisabledFormMixin):
            add_url = reverse('machines:component_create', kwargs={'pk': selected_machine.pk})
            self.fields['component'].help_text = format_html(
                '{}<br><a href="{}">Component missing? Add it to {}</a>',
                self.fields['component'].help_text, add_url, selected_machine)


    def clean(self):
        cleaned_data = super().clean()
        # machine = cleaned_data.get('machine')
        # component = cleaned_data.get('component')
        detected_on = cleaned_data.get('detected_on')
        resolved_on = cleaned_data.get('resolved_on')

        # if machine and component and component.machine_id != machine.pk:
        #     self.add_error('component', 'This c')

        if detected_on and resolved_on and resolved_on < detected_on:
            self.add_error('resolved_on', 'Resolved date cannot be before detection date')
            limited_on = cleaned_data.get('limited_on')
            if limited_on and limited_on > timezone.now():
                self.add_error('limited_on', 'Limited date cannot be in the future')
            if detected_on and limited_on and limited_on < detected_on:
                self.add_error('limited_on', 'Limited date cannot be before detection date')
            if limited_on and resolved_on and resolved_on < limited_on:
                self.add_error('resolved_on',
                               'Resolved date cannot be before the date the machine started running with limitations')

        return cleaned_data


class RepairDeleteForm(DisabledFormMixin, RepairForm):
    pass


class RepairActionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = RepairAction
        exclude = ['created_at',]  #TODO check without exclude auto_now_add field
        labels = {
            'repair': 'Repair',
            'technician': 'Technician',
            'description': 'Description',
        }
        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Describe the action taken'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['repair'].disabled = True

        repair = self.instance.repair if self.instance.pk else self.initial.get('repair')
        if repair is not None:
            self.fields['technician'].queryset = repair.technicians.all()

class RepairSearchForm(BootstrapFormMixin, forms.Form):
    # search by machine; default -> all machines #TODO To think: Better as if with filtering after search?!
    machine = forms.ModelChoiceField(
        queryset=Machine.objects.order_by('model'),
        required=False,
        empty_label='All machines',
        label='',
    )
    query = forms.CharField(
        label='',
        required=False,
        max_length=100,
        help_text='Search by component or problem',
        widget=forms.TextInput(attrs={'placeholder': 'Enter a query'}
        )
    )