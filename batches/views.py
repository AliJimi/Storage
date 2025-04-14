from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import ProductBatch
from .forms import BatchForm
from products.models import Product
from locations.models import Location

def batch_list(request):
    batches = ProductBatch.objects.all().select_related('product', 'location').order_by('-created_at')
    
    context = {
        'batches': batches
    }
    return render(request, 'batches/batch_list.html', context)

def batch_detail(request, pk):
    batch = get_object_or_404(ProductBatch, pk=pk)
    
    # Calculate expiration status
    if batch.expiration_date:
        today = timezone.now().date()
        days_until_expiry = (batch.expiration_date - today).days
        
        if days_until_expiry < 0:
            expiry_status = 'Expired'
            expiry_class = 'danger'
        elif days_until_expiry <= 3:
            expiry_status = 'Critical'
            expiry_class = 'danger'
        elif days_until_expiry <= 7:
            expiry_status = 'Warning'
            expiry_class = 'warning'
        else:
            expiry_status = 'Good'
            expiry_class = 'success'
    else:
        expiry_status = 'No Expiry'
        expiry_class = 'secondary'
    
    context = {
        'batch': batch,
        'expiry_status': expiry_status,
        'expiry_class': expiry_class,
        'effective_price': batch.effective_price,
        'total_value': batch.total_value
    }
    
    return render(request, 'batches/batch_detail.html', context)

def batch_create(request):
    product_id = request.GET.get('product_id')
    
    if request.method == 'POST':
        form = BatchForm(request.POST, product_id=product_id)
        if form.is_valid():
            batch = form.save()
            messages.success(request, f'Batch for "{batch.product.name}" created successfully.')
            return redirect('batch_detail', pk=batch.pk)
    else:
        form = BatchForm(product_id=product_id)
    
    context = {
        'form': form,
        'title': 'Add New Batch'
    }
    
    return render(request, 'batches/batch_form.html', context)

def batch_update(request, pk):
    batch = get_object_or_404(ProductBatch, pk=pk)
    
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            batch = form.save()
            messages.success(request, f'Batch #{batch.id} updated successfully.')
            return redirect('batch_detail', pk=batch.pk)
    else:
        form = BatchForm(instance=batch)
    
    context = {
        'form': form,
        'batch': batch,
        'title': f'Edit Batch: #{batch.id}'
    }
    
    return render(request, 'batches/batch_form.html', context)

def batch_delete(request, pk):
    batch = get_object_or_404(ProductBatch, pk=pk)
    
    if request.method == 'POST':
        product_name = batch.product.name
        batch_id = batch.id
        batch.delete()
        messages.success(request, f'Batch #{batch_id} for "{product_name}" deleted successfully.')
        return redirect('batch_list')
    
    context = {
        'batch': batch
    }
    
    return render(request, 'batches/batch_confirm_delete.html', context)

def batch_list_by_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    batches = ProductBatch.objects.filter(product=product).select_related('location').order_by('-created_at')
    
    context = {
        'batches': batches,
        'product': product,
        'title': f'Batches for {product.name}'
    }
    
    return render(request, 'batches/batch_list_by_product.html', context)

def batch_list_by_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    batches = ProductBatch.objects.filter(location=location).select_related('product').order_by('-created_at')
    
    context = {
        'batches': batches,
        'location': location,
        'title': f'Batches in {location.name}'
    }
    
    return render(request, 'batches/batch_list_by_location.html', context)

def expiring_batches(request):
    today = timezone.now().date()
    days = int(request.GET.get('days', 7))
    target_date = today + timezone.timedelta(days=days)
    
    batches = ProductBatch.objects.filter(
        Q(expiration_date__isnull=False) &
        Q(expiration_date__gte=today) & 
        Q(expiration_date__lte=target_date)
    ).select_related('product', 'location').order_by('expiration_date')
    
    context = {
        'batches': batches,
        'days': days,
        'title': f'Batches Expiring in {days} Days'
    }
    
    return render(request, 'batches/expiring_batches.html', context)