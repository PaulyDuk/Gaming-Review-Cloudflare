// Review approval management functions
// Requires utils.js to be loaded first

function selectAll() { selectAllCheckboxes('.review-checkbox'); }
function deselectAll() { deselectAllCheckboxes('.review-checkbox'); }
function selectAllApproved() { selectAllCheckboxes('.approved-review-checkbox'); }
function deselectAllApproved() { deselectAllCheckboxes('.approved-review-checkbox'); }

function toggleFullReview(link) {
    toggleFullContent(link, 'review-preview', 'full-review');
}
