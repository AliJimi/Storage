from django.shortcuts import render
from django.db.models import Sum, Count, Q
from django.utils import timezone

from products.models import Product
from batches.models import ProductBatch
from locations.models import Location

def dashboard(request):
    # Calculate dashboard statistics
    today = timezone.now().date()
    seven_days_later = today + timezone.timedelta(days=7)
    
    # Basic statistics
    total_products = Product.objects.count()
    active_batches = ProductBatch.objects.filter(quantity__gt=0).count()
    low_stock_items = Product.objects.filter(batches__quantity__lt=10).distinct().count()
    expiring_soon = ProductBatch.objects.filter(
        expiration_date__isnull=False,
        expiration_date__lte=seven_days_later,
        expiration_date__gte=today
    ).count()
    
    # Recent products
    recent_products = Product.objects.order_by('-created_at')[:5]
    
    # Expiring batches
    expiring_batches = ProductBatch.objects.select_related('product', 'location').filter(
        expiration_date__isnull=False,
        expiration_date__lte=seven_days_later,
        expiration_date__gte=today
    ).order_by('expiration_date')[:10]
    
    # Location overview
    locations = Location.objects.filter(level='warehouse')
    
    # Calculate total inventory value
    total_value = ProductBatch.objects.filter(
        sale_price__isnull=False
    ).aggregate(
        total=Sum('quantity') * Sum('sale_price')
    )['total'] or 0
    
    context = {
        'stats': {
            'total_products': total_products,
            'active_batches': active_batches,
            'low_stock_items': low_stock_items,
            'expiring_soon': expiring_soon,
            'total_value': total_value
        },
        'recent_products': recent_products,
        'expiring_batches': expiring_batches,
        'locations': locations,
    }
    
    return render(request, 'dashboard/dashboard.html', context)