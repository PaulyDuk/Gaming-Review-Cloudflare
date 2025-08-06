// Review population and management functions

function selectAll() {
    const checkboxes = document.querySelectorAll('.game-checkbox');
    checkboxes.forEach(checkbox => {
        // Skip disabled checkboxes (games that already have reviews)
        if (!checkbox.disabled) {
            checkbox.checked = true;
            toggleGameData(checkbox, checkbox.value);
        }
    });
    updateCreateButton();
}

function deselectAll() {
    const checkboxes = document.querySelectorAll('.game-checkbox');
    checkboxes.forEach(checkbox => {
        // Skip disabled checkboxes (games that already have reviews)
        if (!checkbox.disabled) {
            checkbox.checked = false;
            toggleGameData(checkbox, checkbox.value);
        }
    });
    updateCreateButton();
}

function toggleGameData(checkbox, index) {
    const row = checkbox.closest('tr');
    const gameDataInput = row.querySelector('.game-data');
    const reviewScoreInput = row.querySelector('.review-score');
    const publishedCheckbox = row.querySelector('.published-checkbox');
    const featuredCheckbox = row.querySelector('.featured-checkbox');
    
    // Check if this game already has a review
    const hasReview = row.classList.contains('table-warning');
    
    if (hasReview) {
        // Disable interaction for games that already have reviews
        checkbox.checked = false;
        checkbox.disabled = true;
        return;
    }
    
    if (checkbox.checked) {
        gameDataInput.disabled = false;
        reviewScoreInput.disabled = false;
        publishedCheckbox.disabled = false;
        featuredCheckbox.disabled = false;
        row.classList.add('table-success');
    } else {
        gameDataInput.disabled = true;
        reviewScoreInput.disabled = true;
        publishedCheckbox.disabled = true;
        featuredCheckbox.disabled = true;
        row.classList.remove('table-success');
    }
    
    updateCreateButton();
}

function updateCreateButton() {
    const checkedBoxes = document.querySelectorAll('.game-checkbox:checked:not(:disabled)');
    const createBtn = document.getElementById('create-reviews-btn');
    
    if (checkedBoxes.length > 0) {
        // Check if all selected games have scores
        let allHaveScores = true;
        checkedBoxes.forEach(checkbox => {
            const row = checkbox.closest('tr');
            const scoreInput = row.querySelector('.review-score');
            if (!scoreInput.value || scoreInput.value === '') {
                allHaveScores = false;
            }
        });
        
        if (allHaveScores) {
            createBtn.disabled = false;
            createBtn.textContent = `Create ${checkedBoxes.length} Review${checkedBoxes.length > 1 ? 's' : ''}`;
        } else {
            createBtn.disabled = true;
            createBtn.textContent = 'Enter scores for all selected games';
        }
    } else {
        createBtn.disabled = true;
        createBtn.textContent = 'Create Selected Reviews';
    }
}

function toggleSummary(link) {
    const summaryDiv = link.closest('.summary-text');
    const fullSummary = summaryDiv.querySelector('.full-summary');
    
    if (fullSummary.style.display === 'none') {
        // Show full summary
        summaryDiv.childNodes[0].style.display = 'none'; // Hide truncated text
        link.style.display = 'none'; // Hide "Show more" link
        fullSummary.style.display = 'block';
    } else {
        // Show truncated summary
        summaryDiv.childNodes[0].style.display = 'inline'; // Show truncated text
        summaryDiv.childNodes[2].style.display = 'inline'; // Show "Show more" link
        fullSummary.style.display = 'none';
    }
}

// Functions for existing reviews bulk actions
function selectAllExisting() {
    const checkboxes = document.querySelectorAll('.existing-review-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = true);
}

function deselectAllExisting() {
    const checkboxes = document.querySelectorAll('.existing-review-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = false);
}

// Form validation - Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add form validation
    const form = document.getElementById('create-reviews-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const checkedBoxes = document.querySelectorAll('.game-checkbox:checked:not(:disabled)');
            if (checkedBoxes.length === 0) {
                e.preventDefault();
                alert('Please select at least one game to create reviews for.');
                return false;
            }
            
            // Check if all selected games have scores
            let missingScores = [];
            checkedBoxes.forEach(checkbox => {
                const row = checkbox.closest('tr');
                const scoreInput = row.querySelector('.review-score');
                const gameTitle = row.querySelector('span').textContent;
                if (!scoreInput.value || scoreInput.value === '') {
                    missingScores.push(gameTitle);
                }
            });
            
            if (missingScores.length > 0) {
                e.preventDefault();
                alert(`Please enter scores for the following games:\n${missingScores.join('\n')}`);
                return false;
            }
            
            // Confirm before proceeding
            if (!confirm(`Are you sure you want to create ${checkedBoxes.length} review(s)? This will generate AI content and may take some time.`)) {
                e.preventDefault();
                return false;
            }
        });
    }
});
