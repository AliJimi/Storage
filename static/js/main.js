// Wait for document to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Initialize all tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // Initialize all popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

    // Handle batch filter form
    const batchFilterForm = document.getElementById('batchFilterForm');
    if (batchFilterForm) {
        batchFilterForm.addEventListener('change', function() {
            this.submit();
        });
    }

    // Handle expiration date warnings
    const expirationDates = document.querySelectorAll('.expiration-date');
    expirationDates.forEach(function(element) {
        const expirationDate = new Date(element.dataset.date);
        const today = new Date();
        const diffTime = expirationDate - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays < 0) {
            element.classList.add('text-danger', 'fw-bold');
            element.title = 'Expired';
        } else if (diffDays <= 7) {
            element.classList.add('text-warning', 'fw-bold');
            element.title = `Expires in ${diffDays} days`;
        }
    });

    // Handle progress bars
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(function(progressBar) {
        const value = parseInt(progressBar.getAttribute('aria-valuenow'));
        if (value >= 90) {
            progressBar.classList.add('bg-danger');
        } else if (value >= 70) {
            progressBar.classList.add('bg-warning');
        } else {
            progressBar.classList.add('bg-success');
        }
    });

    // Handle delete confirmation modals
    const deleteButtons = document.querySelectorAll('.delete-confirm');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemName = this.dataset.name;
            const itemType = this.dataset.type;
            
            if (confirm(`Are you sure you want to delete this ${itemType}: ${itemName}? This action cannot be undone.`)) {
                window.location.href = this.href;
            }
        });
    });
});