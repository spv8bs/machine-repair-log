from django import forms
from common.mixins import DisabledFormMixin
from machines.models import Component, Machine
from repairs.models import Repair, RepairAction


class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = '__all__'
        labels = {
            'machine': 'Machine',
            'component': 'Component',
            'problem': 'Problem',
            'detected_on': 'Detected on',
            'resolved_on': 'Resolved on',
            'diagnosis': 'Diagnosis',
            'cost': 'Cost',
            'photo': 'Photo',
            'technicians': 'Technicians',
            'parts': 'Parts used'
        }
        help_texts = {
            'component': 'Choose a component of the selected machine',
            'resolved_on': 'Leave empty while the repair is still open',
            'cost': 'Total cost of the repair',
            'technicians': 'Technicians of the repair',
            'parts': 'Parts of the repair'
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

        return cleaned_data


class RepairDeleteForm(DisabledFormMixin, RepairForm):
    pass


class RepairActionForm(forms.ModelForm):
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

class RepairSearchForm(forms.Form):
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