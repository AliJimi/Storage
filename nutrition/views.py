from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .models import NutritionData
from .forms import NutritionDataForm
from products.models import Product

def nutrition_list(request):
    nutrition_data = NutritionData.objects.all().select_related('product').order_by('product__name')
    
    context = {
        'nutrition_data_list': nutrition_data
    }
    return render(request, 'nutrition/nutrition_list.html', context)

def nutrition_detail(request, pk):
    nutrition = get_object_or_404(NutritionData, pk=pk)
    
    context = {
        'nutrition': nutrition,
        'product': nutrition.product
    }
    
    return render(request, 'nutrition/nutrition_detail.html', context)

def nutrition_create(request):
    product_id = request.GET.get('product_id')
    
    if request.method == 'POST':
        form = NutritionDataForm(request.POST, product_id=product_id)
        if form.is_valid():
            nutrition = form.save()
            messages.success(request, f'Nutrition data for "{nutrition.product.name}" created successfully.')
            return redirect('nutrition_detail', pk=nutrition.pk)
    else:
        form = NutritionDataForm(product_id=product_id)
    
    context = {
        'form': form,
        'title': 'Add New Nutrition Data'
    }
    
    return render(request, 'nutrition/nutrition_form.html', context)

def nutrition_update(request, pk):
    nutrition = get_object_or_404(NutritionData, pk=pk)
    
    if request.method == 'POST':
        form = NutritionDataForm(request.POST, instance=nutrition)
        if form.is_valid():
            form.save()
            messages.success(request, f'Nutrition data for "{nutrition.product.name}" updated successfully.')
            return redirect('nutrition_detail', pk=nutrition.pk)
    else:
        form = NutritionDataForm(instance=nutrition)
    
    context = {
        'form': form,
        'nutrition': nutrition,
        'title': f'Edit Nutrition Data: {nutrition.product.name}'
    }
    
    return render(request, 'nutrition/nutrition_form.html', context)

def nutrition_delete(request, pk):
    nutrition = get_object_or_404(NutritionData, pk=pk)
    product_name = nutrition.product.name
    
    if request.method == 'POST':
        nutrition.delete()
        messages.success(request, f'Nutrition data for "{product_name}" deleted successfully.')
        return redirect('nutrition_list')
    
    context = {
        'nutrition': nutrition,
        'product': nutrition.product
    }
    
    return render(request, 'nutrition/nutrition_confirm_delete.html', context)

def nutrition_by_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        nutrition = NutritionData.objects.get(product=product)
        return redirect('nutrition_detail', pk=nutrition.pk)
    except NutritionData.DoesNotExist:
        # If nutrition data doesn't exist for this product, redirect to create
        messages.info(request, f'No nutrition data found for {product.name_en}. Create new data below.')
        return redirect(f"{reverse('nutrition_create')}?product_id={product_id}")