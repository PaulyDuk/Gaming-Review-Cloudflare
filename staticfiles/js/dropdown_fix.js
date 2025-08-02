// Fix dropdown hover state persistence issue
document.addEventListener('DOMContentLoaded', function() {
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(function(toggle) {
        // When dropdown is shown, remove focus and blur
        toggle.addEventListener('shown.bs.dropdown', function() {
            this.blur();
        });
        
        // When dropdown is hidden, remove focus and blur
        toggle.addEventListener('hidden.bs.dropdown', function() {
            this.blur();
            // Remove any lingering hover/focus classes
            this.classList.remove('show');
            this.removeAttribute('aria-expanded');
        });
        
        // Remove focus on click
        toggle.addEventListener('click', function() {
            setTimeout(() => {
                this.blur();
            }, 100);
        });
    });
    
    // Close all dropdowns when clicking on another dropdown
    document.addEventListener('click', function(event) {
        if (event.target.matches('.dropdown-toggle')) {
            // Close all other dropdowns
            dropdownToggles.forEach(function(toggle) {
                if (toggle !== event.target && toggle.classList.contains('show')) {
                    const dropdown = new bootstrap.Dropdown(toggle);
                    dropdown.hide();
                    toggle.blur();
                }
            });
        }
    });
});
