window.onload = function() {

	// Dialog initialization
	$(".section-dialog").hide();

	// On-cancel logic
	$("#BUTTON_CANCEL").click(function() {

		// Hide dialogs
		$("#DIALOG_ADD_EDIT").hide()

		// Clear inputs
		$("input").each(function() {
			$(this).val("");
		});

		// Clear dialog events
		$("#BUTTON_SAVE").off("click");
	});

	// Show the "Add Section" dialog
	$("#ADD_SECTION").click(function() {
		$("#DIALOG_ADD_EDIT").show();
		$(".dialog_title").text("Add Section");

		// Do 
		$("#BUTTON_SAVE").on("click.add", function() {
			console.log("save!");
			$.ajax({
				method: "POST",
				url: "/sections/add",
				data: {
					csrf_token: csrfToken,
					day: $("input[name=day]").val(),
					time: $("input[name=time]").val(),
				}
			});
		});
	});
};
