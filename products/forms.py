from django import forms
from .models import Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name_en', 'name_fa', 'barcode', 'category', 'is_edible', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.layout = Layout(
            Row(
                Column('name_en', css_class='col-md-6'),
                Column('barcode', css_class='col-md-6'),
                css_class='mb-3'
            ),
            Row(
                Column('category', css_class='col-md-6'),
                Column('is_edible', css_class='col-md-6 d-flex align-items-center'),
                css_class='mb-3'
            ),
            'description',
            'image',
            Div(
                Submit('submit', 'Save', css_class='btn-primary me-2'),
                css_class='mt-4'
            )
        )