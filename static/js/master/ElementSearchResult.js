$(function() {
    
    $('.list').live('click', function(){
        var data_id = $(this).attr('data-id');
        $(this).toggleClass('selected');
        $.get(AJAX_URL, {'data_id': data_id}, function(html){});
        if ($(this).hasClass('mutex')){
            if($(this).hasClass('selected')){
                $(this).siblings('.mutex').each(function(){
                    $(this).removeClass('selected');
                    });
            }
        }
    });
    
});


$(document).ready(function() { 
		
	$("span.spoiler").hide();
	
	$("a.reveal").live('click', function(){
        var elem = $(this).parents("p").children("span.spoiler");
        if (elem.is(':visible')){
            elem.fadeOut('fast', function(){elem.siblings('.reveal').html('Reveal Plot >>');});
            
        } else{
            elem.fadeIn(2500);
            elem.siblings('.reveal').html('<< Hide Plot');
        }
	});
}); 