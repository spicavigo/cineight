$(document).ready(function() {

	//When page loads...
	$(".tab_content").hide(); //Hide all content
	$("ul.tabs li:first").addClass("active").show(); //Activate first tab
	$(".tab_content:first").show(); //Show first tab content

	//On Click Event
	$("ul.tabs li").click(function() {

		$("ul.tabs li").removeClass("active"); //Remove any "active" class
		$(this).addClass("active"); //Add "active" class to selected tab
		$(".tab_content").hide(); //Hide all tab content

		var activeTab = $(this).find("a").attr("href"); //Find the href attribute value to identify the active tab + content
		$(activeTab).fadeIn(1000); //Fade in the active ID content
		return false;
	});
    //$(".tabs li a").tipTip({maxWidth: "auto"});
    /*$('.tabs li a').each(function(){
        $(this).qtip({
            content: {text: $(this).attr('title')},
            show: 'mouseover',
            hide: 'mouseout'
         });
    });*/
    $('.list_buttons li').each(function(){
        var that = this;
        $(this).qtip({
            content: {text: false},
            show: 'mouseover',
            hide: 'mouseout'
         });
    });
});