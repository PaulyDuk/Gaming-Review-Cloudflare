// Review approval management functions

function selectAll() {
    const checkboxes = document.querySelectorAll('.review-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = true);
}

function deselectAll() {
    const checkboxes = document.querySelectorAll('.review-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = false);
}

function selectAllApproved() {
    const checkboxes = document.querySelectorAll('.approved-review-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = true);
}

function deselectAllApproved() {
    const checkboxes = document.querySelectorAll('.approved-review-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = false);
}

function toggleFullReview(link) {
    const reviewDiv = link.closest('.review-preview');
    const fullReview = reviewDiv.querySelector('.full-review');
    
    if (fullReview.style.display === 'none') {
        fullReview.style.display = 'block';
        link.style.display = 'none';
    } else {
        fullReview.style.display = 'none';
        reviewDiv.querySelector('a').style.display = 'inline';
    }
}
