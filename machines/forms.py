from django import forms
from machines.models import Machine
from common.mixins import BootstrapFormMixin

class MachineForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Machine
        fields = ('model', 'machine_type', 'location', 'is_active', 'notes')

        error_messages ={
            'model': {
                'unique': 'This machine already exists.',
                'required': 'Machine is required.',
            }
        }
        widgets = {
            'model': forms.TextInput(attrs={'placeholder': 'Enter machine model'}),
            'machine_type': forms.TextInput(attrs={'placeholder': 'Enter machine type'}),
        }


