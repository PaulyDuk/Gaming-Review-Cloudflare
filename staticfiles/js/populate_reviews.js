// Enable/disable score and related fields when a game is selected/deselected
function toggleGameData(checkbox, index) {
    const row = checkbox.closest('tr');
    const gameDataInput = row.querySelector('.game-data');
    const reviewScoreInput = row.querySelector('.review-score');
    const publishedCheckbox = row.querySelector('.published-checkbox');
    const featuredCheckbox = row.querySelector('.featured-checkbox');

    // Check if this game already has a review (should be disabled anyway)
    const hasReview = row.classList.contains('table-warning');
    if (hasReview) {
        checkbox.checked = false;
        checkbox.disabled = true;
        return;
    }

    if (checkbox.checked) {
        if (gameDataInput) gameDataInput.disabled = false;
        if (reviewScoreInput) reviewScoreInput.disabled = false;
        if (publishedCheckbox) publishedCheckbox.disabled = false;
        if (featuredCheckbox) featuredCheckbox.disabled = false;
        row.classList.add('table-success');
    } else {
        if (gameDataInput) gameDataInput.disabled = true;
        if (reviewScoreInput) reviewScoreInput.disabled = true;
        if (publishedCheckbox) publishedCheckbox.disabled = true;
        if (featuredCheckbox) featuredCheckbox.disabled = true;
        row.classList.remove('table-success');
    }

    if (typeof updateCreateButton === 'function') {
        updateCreateButton();
    }
}
