from django.contrib import admin
from django.utils import timezone
from datetime import timedelta


class IsExpiredFilter(admin.SimpleListFilter):
    title = 'Is Expired'
    parameter_name = 'is_expired'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Expired'),
            ('no', 'Not expired'),
        )

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == 'yes':
            return queryset.filter(expiration_date__lt=today)
        if self.value() == 'no':
            return queryset.filter(expiration_date__gte=today)
        return queryset


class ExpiresSoonFilter(admin.SimpleListFilter):
    title = 'Expires Soon'
    parameter_name = 'expires_soon'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Expiring Soon'),
            ('no', 'Not soon'),
        )

    def queryset(self, request, queryset):
        soon = timezone.now().date() + timedelta(days=7)
        today = timezone.now().date()
        if self.value() == 'yes':
            return queryset.filter(expiration_date__gte=today, expiration_date__lte=soon)
        if self.value() == 'no':
            return queryset.exclude(expiration_date__gte=today, expiration_date__lte=soon)
        return queryset
