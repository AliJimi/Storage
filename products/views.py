from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum

from .models import Product
from products.forms import ProductForm
from batches.models import ProductBatch
from nutrition.models import NutritionData

def product_list(request):
    products = Product.objects.all().order_by('name')
    
    # Add total quantity information
    for product in products:
        product.total_quantity = product.total_quantity
    
    context = {
        'products': products
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Get batches for this product
    batches = ProductBatch.objects.filter(product=product).order_by('-created_at')
    
    # Get nutrition data if available
    nutrition = None
    try:
        nutrition = NutritionData.objects.get(product=product)
    except NutritionData.DoesNotExist:
        pass
    
    # Calculate total quantity and value
    total_quantity = product.total_quantity
    total_value = sum(
        (batch.sale_price * (1 - batch.discount / 100) * batch.quantity) 
        for batch in batches if batch.sale_price is not None
    )
    
    context = {
        'product': product,
        'batches': batches,
        'nutrition': nutrition,
        'total_quantity': total_quantity,
        'total_value': total_value
    }
    
    return render(request, 'products/product_detail.html', context)

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created successfully.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Add New Product'
    }
    
    return render(request, 'products/product_form.html', context)

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': f'Edit Product: {product.name}'
    }
    
    return render(request, 'products/product_form.html', context)

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully.')
        return redirect('product_list')
    
    context = {
        'product': product
    }
    
    return render(request, 'products/product_confirm_delete.html', context)