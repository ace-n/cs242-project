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

	// Show the "Add Section" dialog
	$("#ADD_SECTION").click(function() {

		// Update UI/variable state
		$("#DIALOG_ADD_EDIT").show();
		$(".dialog-title").text("Add Section");
		window.section_id = null;
	});


	// Show the "Edit Section" dialog
	$(".action-edit").click(function() {

		// Update UI state
		$("#DIALOG_ADD_EDIT").show();
		$(".dialog-title").text("Edit Section");

		// Update input values
		$("input[name=weekday]").val($(this).attr("data-weekday"));
		$("input[name=time]").val($(this).attr("data-time"));
		window.section_id = $(this).attr("data-id");
	});

	// Show the "Delete Confirmation" dialog on delete request
	$(".action-delete").click(function() {
		$("#DIALOG_DELETE").show();
		window.section_id = $(this).attr("data-id");
	});

	// On-Delete (post confirmation) logic
	$("#BUTTON_DELETE").click(function() {
		$(".dialog").hide();
		$.ajax({
			method: "POST",
			url: "/sections/delete",
			data: {
				csrf_token: csrfToken,
				id: window.section_id,
			},
		}).done(function(response) {
			var status = JSON.parse(response);
			if (status["status"] == 200) {
				// Success
				$(".section-details[data-id=" + window.section_id + "]").remove();
			} else {
				// Failure
				alert("ERROR: " + status["message"]);
			}
		});
	});

	// On-Save (post confirmation) logic for add/edit
	$("#BUTTON_SAVE").click(function() {
		$(".dialog").hide()
		var weekday = $("input[name=weekday]").val();
		var time = $("input[name=time]").val();
		$.ajax({
			method: "POST",
			url: "/sections/change",
			data: {
				csrf_token: csrfToken,
				id: window.section_id,
				weekday: weekday,
				time: time,
			}
		}).done(function(response) {
			var status = JSON.parse(response);
			if (status["status"] == 200) {
				// Success - insert new section into page

				// Construct new section
				var new_id = status["message"];
				var c_icon1 = "<i class='fa fa-edit action-edit' data-id='" + new_id + "' data-weekday='" + weekday + "' data-time='" + time + "'></i>";
				var c_icon2 = "<i class='fa fa-remove action-delete' data-id='" + new_id + "'></i>";
				var c_actions = "<div class='section-actions'>" + c_icon1 + c_icon2 + "</div>";

				var c_details = '<div class="section-details" data-id="' + new_id + '">' + time + c_actions + "</div>";

				// Append new section into page
				$(".section-day[data-day='" + weekday + "']").append(c_details);
			} else {
				// Failure
				alert("ERROR: " + status["message"]);
			}
		});
	});
};
