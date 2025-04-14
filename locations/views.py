from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count, Sum

from .models import Location
from .forms import LocationForm
from batches.models import ProductBatch

def location_list(request):
    locations = Location.objects.all().order_by('level', 'name')
    
    context = {
        'locations': locations
    }
    return render(request, 'locations/location_list.html', context)

def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    
    # Get batches in this location
    batches = ProductBatch.objects.filter(location=location).select_related('product').order_by('-created_at')
    
    # Get child locations
    children = Location.objects.filter(parent=location).order_by('name')
    
    # Calculate utilization
    utilization = location.utilization
    
    # Calculate total value
    total_value = location.total_value
    
    context = {
        'location': location,
        'batches': batches,
        'children': children,
        'utilization': utilization,
        'total_value': total_value
    }
    
    return render(request, 'locations/location_detail.html', context)

def location_create(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save()
            messages.success(request, f'Location "{location.name}" created successfully.')
            return redirect('location_detail', pk=location.pk)
    else:
        form = LocationForm()
    
    context = {
        'form': form,
        'title': 'Add New Location'
    }
    
    return render(request, 'locations/location_form.html', context)

def location_update(request, pk):
    location = get_object_or_404(Location, pk=pk)
    
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, f'Location "{location.name}" updated successfully.')
            return redirect('location_detail', pk=location.pk)
    else:
        form = LocationForm(instance=location)
    
    context = {
        'form': form,
        'location': location,
        'title': f'Edit Location: {location.name}'
    }
    
    return render(request, 'locations/location_form.html', context)

def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    
    # Check if location has child locations or batches
    children = Location.objects.filter(parent=location).count()
    batches = ProductBatch.objects.filter(location=location).count()
    
    if request.method == 'POST':
        if children > 0:
            messages.error(request, f'Cannot delete location "{location.name}" because it has {children} child locations.')
            return redirect('location_detail', pk=location.pk)
        
        if batches > 0:
            messages.error(request, f'Cannot delete location "{location.name}" because it has {batches} batches stored.')
            return redirect('location_detail', pk=location.pk)
        
        location_name = location.name
        location.delete()
        messages.success(request, f'Location "{location_name}" deleted successfully.')
        return redirect('location_list')
    
    context = {
        'location': location,
        'children_count': children,
        'batches_count': batches
    }
    
    return render(request, 'locations/location_confirm_delete.html', context)

def location_hierarchy(request):
    # Start with top-level locations (those without parents)
    root_locations = Location.objects.filter(parent__isnull=True).order_by('name')
    
    context = {
        'root_locations': root_locations
    }
    
    return render(request, 'locations/location_hierarchy.html', context)