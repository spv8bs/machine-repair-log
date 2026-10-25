from django import forms

class DisabledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].disabled = True


class DeleteFormInstanceMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs


# Bootstrap styling without form-control or form-select in every widget (EXPERIMENTAL)
# https://www.codegenes.net/blog/add-class-to-form-field-django-modelform/
# https://codemia.io/knowledge-hub/path/define_css_class_in_django_forms
class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                css_class = 'form-check-input'
            elif isinstance(widget, forms.Select):
                css_class = 'form-select'
            else:
                css_class = 'form-control'
            widget.attrs['class'] = f"{widget.attrs.get('class', '')} {css_class}".strip()