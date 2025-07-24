const editUserCommentButtons = document.getElementsByClassName("btn-edit-user-comment");
const userCommentText = document.getElementById("id_body");
const userCommentForm = document.getElementById("userCommentForm");
const submitUserCommentButton = document.getElementById("submitUserCommentButton");
const deleteUserCommentModal = new bootstrap.Modal(document.getElementById("deleteUserCommentModal"));
const deleteUserCommentButtons = document.getElementsByClassName("btn-delete-user-comment");
const deleteUserCommentConfirm = document.getElementById("deleteUserCommentConfirm");

/**
* Initializes edit functionality for the provided edit user comment buttons.
* 
* For each button in the `editUserCommentButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Fetches the content of the corresponding comment.
* - Populates the `userCommentText` input/textarea with the comment's content for editing.
* - Updates the submit button's text to "Update".
* - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
*/
for (let button of editUserCommentButtons) {
  button.addEventListener("click", (e) => {
    let commentId = e.target.getAttribute("comment_id");
    let commentContent = document.getElementById(`user_comment${commentId}`).innerText;
    userCommentText.value = commentContent;
    submitUserCommentButton.innerText = "Update";
    userCommentForm.setAttribute("action", `edit_comment/${commentId}`);
  });
}

/**
* Initializes deletion functionality for the provided delete user comment buttons.
* 
* For each button in the `deleteUserCommentButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Updates the `deleteUserCommentConfirm` link's href to point to the 
* deletion endpoint for the specific comment.
* - Displays a confirmation modal (`deleteUserCommentModal`) to prompt 
* the user for confirmation before deletion.
*/
for (let button of deleteUserCommentButtons) {
  button.addEventListener("click", (e) => {
    let commentId = e.target.getAttribute("comment_id");
    deleteUserCommentConfirm.href = `delete_comment/${commentId}`;
    deleteUserCommentModal.show();
  });
}
