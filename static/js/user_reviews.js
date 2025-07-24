const editReviewButtons = document.getElementsByClassName("btn-edit-review");
const reviewRatingField = document.getElementById("id_rating");
const reviewTextField = document.getElementById("id_review_text");
const reviewForm = document.getElementById("reviewForm");
const submitReviewButton = document.getElementById("submitReviewButton");
const deleteReviewModal = new bootstrap.Modal(document.getElementById("deleteReviewModal"));
const deleteReviewButtons = document.getElementsByClassName("btn-delete-review");
const deleteReviewConfirm = document.getElementById("deleteReviewConfirm");

/**
* Initializes edit functionality for the provided edit review buttons.
* 
* For each button in the `editReviewButtons` collection:
* - Retrieves the associated review's ID upon click.
* - Fetches the content of the corresponding review (rating and text).
* - Populates the `reviewRatingField` and `reviewTextField` with the review's content for editing.
* - Updates the submit button's text to "Update".
* - Sets the form's action attribute to the `edit_review/{reviewId}` endpoint.
*/
for (let button of editReviewButtons) {
  button.addEventListener("click", (e) => {
    let reviewId = e.target.getAttribute("review_id");
    let reviewRating = e.target.getAttribute("review_rating");
    let reviewContentElement = document.getElementById(`review${reviewId}`);
    
    // Get the text content and handle line breaks properly
    let reviewContent = reviewContentElement.querySelector('p').innerHTML;
    // Convert <br> tags back to line breaks for the textarea
    reviewContent = reviewContent.replace(/<br\s*\/?>/gi, '\n');
    // Remove any remaining HTML tags
    reviewContent = reviewContent.replace(/<[^>]*>/g, '');
    // Decode HTML entities
    let tempDiv = document.createElement('div');
    tempDiv.innerHTML = reviewContent;
    reviewContent = tempDiv.textContent || tempDiv.innerText || '';
    
    // Show the form and hide the "already reviewed" message
    const reviewForm = document.getElementById("reviewForm");
    const reviewCompleteMessage = document.getElementById("reviewCompleteMessage");
    const reviewFormTitle = document.getElementById("reviewFormTitle");
    
    if (reviewCompleteMessage) {
      reviewCompleteMessage.style.display = "none";
    }
    if (reviewForm) {
      reviewForm.style.display = "block";
    }
    if (reviewFormTitle) {
      reviewFormTitle.textContent = "Edit Your Review:";
    }
    
    // Populate the form fields
    reviewRatingField.value = reviewRating;
    reviewTextField.value = reviewContent;
    submitReviewButton.innerText = "Update Review";
    reviewForm.setAttribute("action", `edit_review/${reviewId}`);
  });
}

/**
* Initializes deletion functionality for the provided delete review buttons.
* 
* For each button in the `deleteReviewButtons` collection:
* - Retrieves the associated review's ID upon click.
* - Updates the `deleteReviewConfirm` link's href to point to the 
* deletion endpoint for the specific review.
* - Displays a confirmation modal (`deleteReviewModal`) to prompt 
* the user for confirmation before deletion.
*/
for (let button of deleteReviewButtons) {
  button.addEventListener("click", (e) => {
    let reviewId = e.target.getAttribute("review_id");
    deleteReviewConfirm.href = `delete_review/${reviewId}`;
    deleteReviewModal.show();
  });
}
