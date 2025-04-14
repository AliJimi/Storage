from django import forms
from .models import Location
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'level', 'parent', 'address', 'capacity', 'capacity_unit']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Limit parent selection to exclude self and descendants to prevent circular references
        if self.instance.pk:
            descendants = self.get_descendants(self.instance)
            self.fields['parent'].queryset = Location.objects.exclude(
                pk__in=[self.instance.pk] + [d.pk for d in descendants]
            )
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('level', css_class='col-md-6'),
                css_class='mb-3'
            ),
            'parent',
            'address',
            Row(
                Column('capacity', css_class='col-md-6'),
                Column('capacity_unit', css_class='col-md-6'),
                css_class='mb-3'
            ),
            Div(
                Submit('submit', 'Save', css_class='btn-primary me-2'),
                css_class='mt-4'
            )
        )
    
    def get_descendants(self, location):
        """Recursively get all descendants of a location"""
        descendants = []
        children = Location.objects.filter(parent=location)
        
        for child in children:
            descendants.append(child)
            descendants.extend(self.get_descendants(child))
            
        return descendants