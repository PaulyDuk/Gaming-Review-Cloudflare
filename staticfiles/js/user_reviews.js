const editUserReviewButtons = document.getElementsByClassName("btn-edit-user-review");
const userReviewRatingField = document.getElementById("id_rating");
const userReviewTextField = document.getElementById("id_review_text");
const userReviewForm = document.getElementById("userReviewForm");
const submitUserReviewButton = document.getElementById("submitUserReviewButton");
const deleteUserReviewModal = new bootstrap.Modal(document.getElementById("deleteUserReviewModal"));
const deleteUserReviewButtons = document.getElementsByClassName("btn-delete-user-review");
const deleteUserReviewConfirm = document.getElementById("deleteUserReviewConfirm");

/**
* Initializes edit functionality for the provided edit user review buttons.
* 
* For each button in the `editUserReviewButtons` collection:
* - Retrieves the associated review's ID upon click.
* - Fetches the content of the corresponding review.
* - Populates the `userReviewTextField` and `userReviewRatingField` with the review's content for editing.
* - Updates the submit button's text to "Update".
* - Sets the form's action attribute to the `edit_review/{reviewId}` endpoint.
*/
for (let button of editUserReviewButtons) {
  button.addEventListener("click", (e) => {
    let reviewId = e.target.getAttribute("review_id");
    let reviewRating = e.target.getAttribute("review_rating");
    let reviewContent = document.getElementById(`user_review${reviewId}`).innerText;
    
    // Show the form and hide the "already reviewed" message
    const reviewCompleteMessage = document.getElementById("reviewCompleteMessage");
    const userReviewFormContainer = document.getElementById("userReviewFormContainer");
    
    if (reviewCompleteMessage) {
      reviewCompleteMessage.style.display = "none";
    }
    if (userReviewFormContainer) {
      userReviewFormContainer.style.display = "block";
    }
    
    userReviewRatingField.value = reviewRating;
    userReviewTextField.value = reviewContent;
    submitUserReviewButton.innerText = "Update";
    userReviewForm.setAttribute("action", `edit_review/${reviewId}`);
  });
}

/**
* Initializes deletion functionality for the provided delete user review buttons.
* 
* For each button in the `deleteUserReviewButtons` collection:
* - Retrieves the associated review's ID upon click.
* - Updates the `deleteUserReviewConfirm` link's href to point to the 
* deletion endpoint for the specific review.
* - Displays a confirmation modal (`deleteUserReviewModal`) to prompt 
* the user for confirmation before deletion.
*/
for (let button of deleteUserReviewButtons) {
  button.addEventListener("click", (e) => {
    let reviewId = e.target.getAttribute("review_id");
    deleteUserReviewConfirm.href = `delete_review/${reviewId}`;
    deleteUserReviewModal.show();
  });
}
