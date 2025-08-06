// Comment approval management functions

function selectAll() {
    const checkboxes = document.querySelectorAll('.comment-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = true);
}

function deselectAll() {
    const checkboxes = document.querySelectorAll('.comment-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = false);
}

function selectAllApproved() {
    const checkboxes = document.querySelectorAll('.approved-comment-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = true);
}

function deselectAllApproved() {
    const checkboxes = document.querySelectorAll('.approved-comment-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = false);
}

function toggleFullComment(link) {
    const commentDiv = link.closest('.comment-preview');
    const fullComment = commentDiv.querySelector('.full-comment');
    
    if (fullComment.style.display === 'none') {
        fullComment.style.display = 'block';
        link.style.display = 'none';
    } else {
        fullComment.style.display = 'none';
        commentDiv.querySelector('a').style.display = 'inline';
    }
}
