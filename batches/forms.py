from django import forms
from .models import ProductBatch
from nutrition.models import NutritionData
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Fieldset

class BatchForm(forms.ModelForm):
    class Meta:
        model = ProductBatch
        fields = [
            'product', 'quantity', 'expiration_date', 
            'location', 'min_temperature', 'max_temperature',
            'purchase_price', 'sale_price', 'discount',
            'nutrition_data'
        ]
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        
        # If product_id is provided, preset the product field and filter nutrition data
        if product_id:
            self.fields['product'].initial = product_id
            self.fields['product'].widget.attrs['readonly'] = True
            self.fields['nutrition_data'].queryset = NutritionData.objects.filter(product_id=product_id)
        elif self.instance and self.instance.pk:
            # If we're editing an existing batch, filter nutrition data
            self.fields['nutrition_data'].queryset = NutritionData.objects.filter(
                product_id=self.instance.product_id
            )
        else:
            # Empty form - no need to show nutrition data yet
            self.fields['nutrition_data'].queryset = NutritionData.objects.none()
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='col-md-6'),
                Column('quantity', css_class='col-md-6'),
                css_class='mb-3'
            ),
            Row(
                Column('expiration_date', css_class='col-md-6'),
                Column('location', css_class='col-md-6'),
                css_class='mb-3'
            ),
            Fieldset(
                'Temperature Requirements',
                Row(
                    Column('min_temperature', css_class='col-md-6'),
                    Column('max_temperature', css_class='col-md-6'),
                    css_class='mb-3'
                ),
            ),
            Fieldset(
                'Pricing Information',
                Row(
                    Column('purchase_price', css_class='col-md-4'),
                    Column('sale_price', css_class='col-md-4'),
                    Column('discount', css_class='col-md-4'),
                    css_class='mb-3'
                ),
            ),
            'nutrition_data',
            Div(
                Submit('submit', 'Save', css_class='btn-primary me-2'),
                css_class='mt-4'
            )
        )