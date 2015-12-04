// Show the "Delete Confirmation" dialog on delete request
// NOTE: Delete event handlers must be reinitialized when elements are added
window.refresh_deletes = function() {
	$(".action-delete").off('click').on('click',function() {
		window.email = $(this).attr('data-email');
		$("#DIALOG_DELETE").show();
	});
};

// Main jQuery logic
window.onload = function() {

	// Dialog initialization
	$(".section-dialog").hide();

	// On-cancel logic
	$(".BUTTON_CANCEL").click(function() {

		// Hide dialogs
		$(".dialog").hide();

		// Clear inputs
		$("input").each(function() {
			$(this).val("");
		});
	});

	// Initialize deletes
	window.refresh_deletes()

	// Show the "Add User" dialog
	$(".add-user").click(function() {

		// Update UI/variable state
		$("#DIALOG_ADD").show();
	});

	// Show the "Add User" dialog for Password Users
	$("#ADD_PASSWORD_USER").click(function() {
		$("#DIALOG_ADD .dialog-title").text("Add Password User");
		window.is_new_user_passworded = true;
	});

	// Show the "Add User" dialog for Authcode Users
	$("#ADD_AUTHCODE_USER").click(function() {
		$("#DIALOG_ADD .dialog-title").text("Add Authcode User");
		window.is_new_user_passworded = false;
	});

	// On-Delete (post confirmation) logic
	$("#BUTTON_DELETE").click(function() {
		$(".dialog").hide();
		$.ajax({
			method: "POST",
			url: "/users/delete",
			data: {
				csrf_token: csrfToken,
				email: window.email
			},
		}).done(function(response) {
			var status = JSON.parse(response);
			if (status["status"] == 200) {
				// Success - remove deleted item from page
				$('.user-item[data-email="' + window.email + '"]').remove();
			} else {
				// Failure
				alert("ERROR! " + status["message"]);
			}
		});
	});

	// On-Save (post confirmation) logic for add/edit
	$("#BUTTON_SAVE").click(function() {
		$(".dialog").hide();
		window.email = $("input[name=email]").val();
		$.ajax({
			method: "POST",
			url: "/users/add",
			data: {
				csrf_token: csrfToken,
				email: $("input[name=email]").val(),
				is_passworded: window.is_new_user_passworded
			}
		}).done(function(response) {	
			var status = JSON.parse(response);
			if (status["status"] == 200) {
				// Success - add added item to page
				var parent = $("#" + (window.is_new_user_passworded ? "PASSWORD" : "AUTHCODE") + "_USERS");
				// Construct children
				var email_child = "<div class='user-email'>" + window.email + "</div>";
				var icon_child = "<i class='action-delete fa fa-remove' data-email='" + window.email + "'></i>";

				// Add user item to document
				parent.append("<div class='user-item' data-email='" + window.email + "'>" + email_child + icon_child + "</div>");

				// Refresh deletes
				window.refresh_deletes();
			} else {
				// Failure
				alert("ERROR! " + status["message"]);
			}
		});	
	});
};
