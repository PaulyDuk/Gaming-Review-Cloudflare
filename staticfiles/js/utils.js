// Shared utility functions for checkboxes and toggling full content

/**
 * Select all checkboxes matching a selector
 */
function selectAllCheckboxes(selector) {
    document.querySelectorAll(selector).forEach(checkbox => {
        if (!checkbox.disabled) checkbox.checked = true;
    });
}

/**
 * Deselect all checkboxes matching a selector
 */
function deselectAllCheckboxes(selector) {
    document.querySelectorAll(selector).forEach(checkbox => {
        if (!checkbox.disabled) checkbox.checked = false;
    });
}

/**
 * Toggle full content display for a preview element
 * @param {HTMLElement} link - The link/button clicked
 * @param {string} previewClass - The preview container class
 * @param {string} fullClass - The full content class
 */
function toggleFullContent(link, previewClass, fullClass) {
    const previewDiv = link.closest('.' + previewClass);
    const fullContent = previewDiv.querySelector('.' + fullClass);
    if (fullContent.style.display === 'none' || !fullContent.style.display) {
        fullContent.style.display = 'block';
        link.style.display = 'none';
    } else {
        fullContent.style.display = 'none';
        previewDiv.querySelector('a').style.display = 'inline';
    }
}
