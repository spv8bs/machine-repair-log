from django import forms
from machines.models import Machine, Component
from common.mixins import BootstrapFormMixin, DisabledFormMixin

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


class ComponentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Component
        fields = '__all__'
        labels = {
            'component_type': 'Component',
            'parts': 'Parts',
        }
        help_texts = {
            'parts': 'Parts that fit this component (hold Ctrl to select more than one)'
        }
        widgets = {
            'component_type': forms.TextInput(attrs={'placeholder': 'Enter component'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional description'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['machine'].disabled = True

class ComponentDeleteForm(DisabledFormMixin, ComponentForm):
    pass