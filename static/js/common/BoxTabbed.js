$(document).ready(function() {

	//When page loads...
	$(".tab_content").hide(); //Hide all content
	$("ul.tabs li:first").addClass("active").show(); //Activate first tab
	$(".tab_content:first").show(); //Show first tab content

	//On Click Event
	$("ul.tabs li").click(function() {

        var orig = $("ul.tabs li.active a").attr('href');
		$("ul.tabs li").removeClass("active"); //Remove any "active" class
		$(this).addClass("active"); //Add "active" class to selected tab

		var activeTab = $(this).find("a").attr("href"); //Find the href attribute value to identify the active tab + content
        $(orig).fadeOut(2000); //Hide all tab content
		$(activeTab).fadeIn(2000); //Fade in the active ID content
		return false;
	});
    $(".tabs li a").tipTip({maxWidth: "auto"});
});