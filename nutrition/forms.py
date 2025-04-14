from django import forms
from .models import NutritionData
from products.models import Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Fieldset

class NutritionDataForm(forms.ModelForm):
    class Meta:
        model = NutritionData
        fields = [
            'product', 'serving_size',
            'calories_per_serving', 'protein_per_serving', 'fat_per_serving', 'carbs_per_serving',
            'calories_total', 'protein_total', 'fat_total', 'carbs_total',
            'ingredients', 'allergens'
        ]
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 3}),
            'allergens': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        
        # Only show edible products or force them to be edible
        self.fields['product'].queryset = Product.objects.filter(is_edible=True)
        
        # If product_id is provided, preset the product field
        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                if not product.is_edible:
                    product.is_edible = True
                    product.save()
                self.fields['product'].initial = product
                self.fields['product'].widget.attrs['readonly'] = True
            except Product.DoesNotExist:
                pass
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='col-md-6'),
                Column('serving_size', css_class='col-md-6'),
                css_class='mb-4'
            ),
            Fieldset(
                'Nutritional Values Per Serving',
                Row(
                    Column('calories_per_serving', css_class='col-md-3'),
                    Column('protein_per_serving', css_class='col-md-3'),
                    Column('fat_per_serving', css_class='col-md-3'),
                    Column('carbs_per_serving', css_class='col-md-3'),
                    css_class='mb-3'
                ),
            ),
            Fieldset(
                'Nutritional Values Total',
                Row(
                    Column('calories_total', css_class='col-md-3'),
                    Column('protein_total', css_class='col-md-3'),
                    Column('fat_total', css_class='col-md-3'),
                    Column('carbs_total', css_class='col-md-3'),
                    css_class='mb-3'
                ),
            ),
            Fieldset(
                'Additional Information',
                'ingredients',
                'allergens',
            ),
            Div(
                Submit('submit', 'Save', css_class='btn-primary me-2'),
                css_class='mt-4'
            )
        )