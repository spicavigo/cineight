$(function(){

	$("ul.subnav").parent().append("<span></span>"); //Only shows drop down trigger when js is enabled (Adds empty span tag after ul.subnav*)

	$("ul.topnav > li > a").click(function() { //When trigger is clicked...
		if ($(this).parent().find("ul.subnav").length){
		//Following events are applied to the subnav itself (moving subnav up and down)
			$(this).parent().find("ul.subnav").toggle(); //Drop down the subnav on click
			$(this).parent().toggleClass('selected');
			console.log(123);
			return false;
		}
		//Following events are applied to the trigger (Hover events for the trigger)
	});

});
