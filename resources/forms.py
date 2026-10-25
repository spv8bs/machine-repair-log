from common.mixins import DisabledFormMixin
from django import forms
from resources.models import Technician, Supplier, Part


class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = '__all__'

        error_messages = {
            'first_name': {'required': 'Please enter first name.'},
            'last_name': {'required': 'Please enter last name.'},
            'position': {'required': 'Please enter position.'},
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name.'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name.'}),
            'position': forms.TextInput(attrs={'placeholder': 'Enter position.'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email.'}),
        }

class TechnicianDeleteForm(DisabledFormMixin, TechnicianForm):
    pass

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

        error_messages = {
            'name': {'required': 'Please enter supplier name.'},
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter supplier name.'}),
            'contact_person': forms.TextInput(attrs={'placeholder': 'Enter contact person.'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter supplier email.'}),
        }

class SupplierDeleteForm(DisabledFormMixin, SupplierForm):
    pass

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = '__all__'

        error_messages = {
            'name': {'required': 'Please enter part name.'},
            'catalog_number': {
                'unique': 'A part with this number already exists.',
                'required': 'Please enter part catalog_number.'},
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter part name.'}),
            'catalog_number': forms.TextInput(attrs={'placeholder': 'Enter catalog_number.'}),
            'unit_price': forms.NumberInput(attrs={'placeholder': 'Enter unit price.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.order_by('name')

class PartDeleteForm(DisabledFormMixin, PartForm):
    pass
