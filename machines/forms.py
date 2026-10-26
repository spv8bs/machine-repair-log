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

    def clean_location(self):
        location = self.cleaned_data['location']
        return ' '.join(location.split()).capitalize()


class MachineFilterForm(BootstrapFormMixin, forms.Form):
    location = forms.ChoiceField(required=False, label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        locations = (Machine.objects.exclude(location='')
                     .order_by('location')
                     .values_list('location', flat=True)
                     .distinct())
        self.fields['location'].choices = [('', 'All locations')] + [(location, location) for location in locations]


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