// Comment approval management functions
// Requires utils.js to be loaded first

function selectAll() { selectAllCheckboxes('.comment-checkbox'); }
function deselectAll() { deselectAllCheckboxes('.comment-checkbox'); }
function selectAllApproved() { selectAllCheckboxes('.approved-comment-checkbox'); }
function deselectAllApproved() { deselectAllCheckboxes('.approved-comment-checkbox'); }

function toggleFullComment(link) {
    toggleFullContent(link, 'comment-preview', 'full-comment');
}
